import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib import messages
from events import logger
from events.forms import EventForm, GuestForm
from events.models import Event, Guest


class ListEventView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    permission_required = ['events.view_event']
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all().filter(end_date__gt=datetime.date.today())


class NewEventView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    permission_required = ['events.add_event']
    form_class = EventForm


class DetailEventView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    permission_required = ['events.view_event']

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
    success_url = reverse_lazy('events:event-list')


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
                return redirect('events:event-detail', event.pk)
        guest, _ = Guest.objects.get_or_create(person=person, event=event)
        guest.status = 'REGISTERED'
        guest.save()
        messages.success(self.request, 'Вы зарегистрированы на мероприятие')
        return redirect('events:event-detail', event.pk)


class CancelView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Guest
    permission_required = ['events.view_event', 'events.delete_guest']

    def form_valid(self, form):
        self.object.status = 'REFUSED'
        self.object.refused_time = datetime.datetime.now()
        self.object.save()
        messages.info(self.request, 'Регистрация отменена')
        return redirect('events:event-detail', self.object.event.pk)

class UpdateEventView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    permission_required = ['events.change_event']
    form_class = EventForm
