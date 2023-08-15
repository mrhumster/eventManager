import base64
import datetime
import os.path

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.files import File
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.dateparse import parse_datetime
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, FormView, TemplateView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.tasks import send_email
from eventManager.settings import SITE_SCHEMA
from events import logger
from events.forms import EventForm, GuestForm, NewGuestForm, ExistingGuestForm, SetVisitedConfirmForm
from events.models import Event, Guest, Task
from events.serializers import TaskSerializer, EventSerializer, GuestSerializer, VisitSerializer


class ListEventView(ListView):
    model = Event
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all().filter(end_date__gte=datetime.date.today())


class NewEventView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    permission_required = ['events.add_event']
    form_class = EventForm
    success_url = reverse_lazy('events:events')


class DetailEventView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(DetailEventView, self).get_context_data(**kwargs)
        guest_list = self.object.guest_set.all()
        context['guest'] = False
        for guest in guest_list:
            if self.request.user == guest.person:
                context['guest'] = guest
        return context


class DeleteEventView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    permission_required = ['events.delete_event']
    success_url = reverse_lazy('events:events')


class RegisterView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Guest
    permission_required = ['events.view_event', 'events.add_guest']
    form_class = GuestForm

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        event_pk = self.request.path.partition('/register')[0][1:]
        event = Event.objects.get(pk=event_pk)
        context['event'] = event
        return context

    def post(self, *args, **kwargs):
        event = Event.objects.get(pk=self.request.path.partition('/register')[0][1:])
        person = self.request.user
        for guest in person.guest_set.all():
            if guest.event == event and guest.status in ('REGISTERED', 'VISITED'):
                messages.info(self.request, 'Вы уже зарегистрированы на мероприятии')
                return redirect('events:event', event.pk)
        guest, _ = Guest.objects.get_or_create(person=person, event=event)
        guest.status = 'REGISTERED'
        guest.save()
        messages.success(self.request, 'Вы зарегистрированы на мероприятие')
        return redirect('events:event', event.pk)


class CancelView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Guest
    permission_required = ['events.view_event', 'events.delete_guest']

    def form_valid(self, form):
        self.object.status = 'REFUSED'
        self.object.save()
        messages.info(self.request, 'Регистрация отменена')
        return redirect('events:event', self.object.event.pk)

class UpdateEventView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    permission_required = ['events.change_event']
    form_class = EventForm
    def get_success_url(self):
        return reverse('events:event', kwargs={'pk': self.object.pk})

class AddGuestView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ['events.add_guest', 'events.view_event', 'events.change_event']
    form_class = NewGuestForm
    template_name = 'events/new_guest_form.html'


    def get_context_data(self, **kwargs):
        context = super(AddGuestView, self).get_context_data(**kwargs)
        event_pk = self.request.path.partition('/add-guest')[0][1:]
        event = Event.objects.get(pk=event_pk)
        context['event'] = event
        return context

    def form_valid(self, form):
        event = Event.objects.get(pk=self.request.path.partition('/add-guest')[0][1:])
        username = form.cleaned_data.get('email').partition('@')[0]
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        person, _ = User.objects.get_or_create(email=email)

        if _:
            logger.info(f'Создан новый пользователь: {person}')
            person.username = username
            person.first_name = first_name
            person.last_name = last_name
            person.groups.add(Group.objects.get(name='user'))
            password = User.objects.make_random_password()
            person.set_password(password)
            person.save()
            msg = {
                'subject': f'🔒 Ваш пароль для входа',
                'body': f'{person.username} {password}',
                'recipients': [person.email],
                'template': 'messages/forgot_password.html',
                'url': f"{SITE_SCHEMA}://{Site.objects.get_current().domain}",
                'check_email_verified': False
            }
            send_email.delay(**msg)

        guest, _ = Guest.objects.get_or_create(person=person, event=event)

        if _:
            logger.info(f'Создан новый гость: {guest}')
        guest.status = 'REGISTERED'
        guest.save()


        return redirect('events:event', event.pk)


class DetailGuestListView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    permission_required = ['events.view_event', 'events.view_guest', 'events.change_guest', 'events.delete_guest']
    template_name = 'events/event_guest_detail.html'


class RegisterRefusedGuestView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ['events.view_event', 'events.view_guest', 'events.change_guest']
    form_class = ExistingGuestForm
    template_name = 'events/guest_refused_form.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterRefusedGuestView, self).get_context_data(**kwargs)
        guest_pk = self.request.path.partition('/register/')[2][:-1]
        guest = Guest.objects.get(pk=guest_pk)
        context['guest'] = guest
        return context

    def form_valid(self, form):
        event_pk = self.request.path.partition('/register/')[0][1:]
        guest_pk = self.request.path.partition('/register/')[2][:-1]
        guest = Guest.objects.get(id=guest_pk)
        guest.status = 'REGISTERED'
        guest.save()
        send_alert = form.cleaned_data.get('send_alert')
        if send_alert:
            body = f"""
            Добрый день, {guest.person.first_name} {guest.person.last_name}!
            {self.request.user.first_name} {self.request.user.last_name} зарегистрировал вас на мероприятие: 
            {guest.event.title}. Будем ждать вас {guest.event.start_date} в {guest.event.start_time}.
            """
            msg = {
                'subject': f'Вы зарегистрированы на мероприятие: {guest.event.title}',
                'body': body,
                'recipients': [guest.person.email],
                'template': 'messages/email.html',
                'check_email_verified': False
            }
            send_email.delay(**msg)
            messages.info(self.request, 'Уведомление о регистрации пользователю отправлено')

        return redirect('events:event', event_pk)

class SetVisitedGuestView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ['events.view_event', 'events.view_guest', 'events.change_guest']
    form_class = SetVisitedConfirmForm
    template_name = 'events/guest_visited_form.html'

    def get_context_data(self, **kwargs):
        context = super(SetVisitedGuestView, self).get_context_data(**kwargs)
        guest_pk = self.request.path.partition('/visited/')[2][:-1]
        guest = Guest.objects.get(pk=guest_pk)
        context['guest'] = guest
        return context

    def form_valid(self, form):
        event_pk = self.request.path.partition('/visited/')[0][1:]
        guest_pk = self.request.path.partition('/visited/')[2][:-1]
        guest = Guest.objects.get(id=guest_pk)
        guest.status = 'VISITED'
        guest.save()
        return redirect('events:guest-list', event_pk)

class DetailGuestView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Guest


class CancelRegisteredGuestView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ['events.view_event', 'events.view_guest', 'events.change_guest']
    form_class = ExistingGuestForm
    template_name = 'events/guest_registered_form.html'

    def get_context_data(self, **kwargs):
        context = super(CancelRegisteredGuestView, self).get_context_data(**kwargs)
        guest_pk = self.request.path.partition('/cancel/')[2][:-1]
        guest = Guest.objects.get(pk=guest_pk)
        context['guest'] = guest
        return context

    def form_valid(self, form):
        event_pk = self.request.path.partition('/cancel/')[0][1:]
        guest_pk = self.request.path.partition('/cancel/')[2][:-1]
        guest = Guest.objects.get(id=guest_pk)
        guest.status = 'REFUSED'
        guest.save()
        send_alert = form.cleaned_data.get('send_alert')
        if send_alert:
            body = f"""
                        Добрый день, {guest.person.first_name} {guest.person.last_name}!
                        {self.request.user.first_name} {self.request.user.last_name} отменил регистрацию на мероприятие: 
                        {guest.event.title}. Если возникли вопросы, напишите на: {self.request.user.email}.
                        """
            msg = {
                'subject': f'Регистрация отменена: {guest.event.title}',
                'body': body,
                'recipients': [guest.person.email],
                'template': 'messages/email.html',
                'check_email_verified': False
            }
            send_email.delay(**msg)
            messages.info(self.request, 'Уведомление об отмене регистрации пользователю отправлено')
        return redirect('events:guest-list', event_pk)


class TasksList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'events/event_task.html'
    permission_required = ['events.view_event', 'events.view_guest', 'events.change_guest', 'events.view_task']

    def get_context_data(self, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)
        event_pk = self.request.path.partition('/tasks/')[0][1:]
        event = Event.objects.get(pk=event_pk)
        context['event'] = event
        context['login_guest_id'] = self.request.user.guest_set.first().id
        return context

class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(methods=['get'], detail=True)
    def guests(self, request, pk):
        event = Event.objects.get(id=pk)
        serializer = GuestSerializer(event.guest_set.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        etag = request.headers.get('ETag', '')
        last_modified = parse_datetime(etag)
        if last_modified == instance.change_time:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        return Response(serializer.data, headers={'ETag': instance.change_time})



class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

class GuestViewSet(ModelViewSet):
    serializer_class = GuestSerializer
    queryset = Guest.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(methods=['post', 'get'], detail=False)
    def visit(self, request):
        if request.method == 'POST':
            serializer = VisitSerializer(data=request.data)
            if serializer.is_valid():
                event = Event.objects.get(id=serializer.validated_data['event_id'])
                try:
                    guest = Guest.objects.get(person__first_name=serializer.validated_data['first_name'],
                                          person__last_name=serializer.validated_data['last_name'],
                                          person__email=serializer.validated_data['email'],
                                          event=event,
                                          person__is_staff=False)
                    if guest.status == Guest.VISITED:
                        return Response({
                            'message': f'{guest.person.first_name} {guest.person.last_name} уже проходил на мероприятие {guest.event.title}'
                        },
                            status=status.HTTP_400_BAD_REQUEST)
                except Guest.DoesNotExist:
                    new_user, _ = User.objects.get_or_create(
                        first_name=serializer.validated_data['first_name'],
                        last_name=serializer.validated_data['last_name'],
                        email=serializer.validated_data['email'],
                        username=serializer.validated_data['email'].partition('@')[0]
                    )
                    if _:
                        logger.info(f'Создан новый пользователь: {new_user}')
                    guest = Guest.objects.create(event=event, person=new_user, status=Guest.REGISTERED)

                guest.status = Guest.VISITED
                guest.save()
                imgstr64 = serializer.validated_data['image']
                if imgstr64:
                    imgdata = base64.b64decode(imgstr64)
                    fname = '/tmp/%s.jpg' % (str(guest.id))
                    with open(fname, 'wb') as f:
                        f.write(imgdata)
                    imgname = '%s.jpg' % (str(guest.id))
                    guest.image.save(imgname, File(open(fname, 'br')))
                    os.remove(fname)
                guest_serializer = GuestSerializer(guest)
                return Response(guest_serializer.data, status=status.HTTP_200_OK)
            else:
                logger.info(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
