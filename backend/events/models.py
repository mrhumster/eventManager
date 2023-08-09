import datetime

from django.db import models

from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from events import logger


class Event(models.Model):
    title = models.CharField(verbose_name='Название мероприятия', max_length=200)
    description = models.TextField(verbose_name='Описание')
    start_time = models.TimeField(verbose_name='Время начала мероприятия')
    start_date = models.DateField(verbose_name='Дата начала мероприятия', default=datetime.date.today)
    end_time = models.TimeField(verbose_name='Время окончание мероприятия')
    end_date = models.DateField(verbose_name='Дата окончание мероприятия', default=datetime.date.today)
    change_time = models.DateTimeField(verbose_name='Время изменения', default=timezone.now())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'pk': self.id})

    def get_managers(self):
        return self.guest_set.all().filter(person__is_staff=True)

    def get_guests(self):
        return self.guest_set.all().filter(person__is_staff=False)

    class Meta:
        ordering = ['start_date']

class Guest(models.Model):
    REGISTERED = 'REGISTERED'
    VISITED = 'VISITED'
    REFUSED = 'REFUSED'

    GUEST_STATUS_CHOICES = (
        (REGISTERED, 'Зарегистрирован'),
        (VISITED, 'На мероприятии'),
        (REFUSED, 'Отмена регистрации')
    )
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=GUEST_STATUS_CHOICES, max_length=15)
    registered_time = models.DateTimeField(verbose_name='Время регистрации', auto_now_add=True)
    visited_time = models.DateTimeField(verbose_name='Время посещения', null=True, blank=True)
    refused_time = models.DateTimeField(verbose_name='Время отказа', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    change_time = models.DateTimeField(verbose_name='Время изменения', auto_now=True)
    image = models.ImageField(upload_to='guests', blank=True, max_length=255)

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name} - {self.event.title}'

    def make_task(self):
        if not self.person.is_staff:
            task, created = Task.objects.get_or_create(event=self.event, guest=self, description=Task.MERCH)
            if created:
                logger.info(f"Создана новая задача: {task=}")
            else:
                logger.info(f"Уже существует задача: {task=}")
                if task.status != Task.CLOSED:
                    task.status = Task.NEW
                    task.save()
                
        else:
            logger.info('Для организаторов задачи не требуется')

    def remove_task(self):
        if not self.person.is_staff:
            for task in self.guest_task_set.all():
                task.status = Task.CANCEL
                task.save()

    class Meta:
        ordering = ['-person']


class Task(models.Model):

    NEW = 'NEW'
    PROGRESS = 'PROGRESS'
    CLOSED = 'CLOSED'
    CANCEL = 'CANCEL'

    TASK_STATUS = {
        (NEW, 'Новая задача'),
        (PROGRESS, 'Задача в работе'),
        (CLOSED, 'Задача завершена'),
        (CANCEL, 'Задача отменена')
    }

    MERCH = 'MERCH'

    TASK_DESCRIPTION = {
        (MERCH, 'Выдать раздаточный материал')
    }

    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='guest_task_set', verbose_name='Гость')
    executor = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, related_name='my_task_set', verbose_name='Исполнитель задачи', blank=True)
    description = models.TextField(verbose_name='Описание задачи', choices=TASK_DESCRIPTION, default=MERCH)
    created_time = models.DateTimeField(verbose_name='Время создания задачи', auto_now_add=True)
    progress_time = models.DateTimeField(verbose_name='Время взятия в работу', null=True, blank=True)
    closed_time = models.DateTimeField(verbose_name='Время завершения задачи', null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name='Время отмены задачи', null=True, blank=True)
    status = models.CharField(verbose_name='Статус задачи', choices=TASK_STATUS, default=NEW)
    change_time = models.DateTimeField(verbose_name='Время изменения', auto_now=True)

    def __str__(self):
        return f'{self.pk} - {self.status } - {self.guest.person.first_name} {self.guest.person.last_name} - {self.event.title}'

    def save(self, *args, **kwargs):
        self.event.change_time = timezone.now()
        self.event.save()
        logger.info(self.event.change_time)
        return super(Task, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']


@receiver(signals.post_init, sender=Guest)
def post_init_guest_handler(sender, instance, **kwargs):
    instance.post_init_status = instance.status

@receiver(signals.pre_save, sender=Guest)
def pre_init_guest_handler(sender, instance, **kwargs):
    if instance.post_init_status != instance.status:
        match instance.status:
            case Guest.VISITED:
                instance.visited_time = timezone.now()
                instance.make_task()
            case Guest.REFUSED:
                instance.remove_task()
                instance.refused_time = timezone.now()
            case Guest.REGISTERED:
                instance.remove_task()

@receiver(signals.post_init, sender=Task)
def post_init_task_handler(sender, instance, **kwargs):
    instance.post_init_status = instance.status


@receiver(signals.pre_save, sender=Task)
def pre_save_task_handler(sender, instance, **kwargs):
    if instance.post_init_status != instance.status:
        match instance.status:
            case Task.PROGRESS:
                instance.progress_time = timezone.now()
            case Task.CANCEL:
                instance.cancel_time = timezone.now()
            case Task.CLOSED:
                instance.closed_time = timezone.now()
