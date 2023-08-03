import datetime

from django.db import models

from django.conf import settings
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(verbose_name='Название мероприятия', max_length=200)
    description = models.TextField(verbose_name='Описание')
    start_time = models.TimeField(verbose_name='Время начала мероприятия')
    start_date = models.DateField(verbose_name='Дата начала мероприятия', default=datetime.date.today)
    end_time = models.TimeField(verbose_name='Время окончание мероприятия')
    end_date = models.DateField(verbose_name='Дата окончание мероприятия', default=datetime.date.today)

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
    GUEST_STATUS_CHOICES = (
        ('REGISTERED', 'Зарегистрирован'),
        ('VISITED', 'На мероприятии'),
        ('REFUSED', 'Отмена регистрации')
    )
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=GUEST_STATUS_CHOICES, max_length=15)
    registered_time = models.DateTimeField(verbose_name='Время регистрации', auto_now_add=True)
    visited_time = models.DateTimeField(verbose_name='Время посещения', null=True)
    refused_time = models.DateTimeField(verbose_name='Время отказа', null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name} - {self.event.title}'


    class Meta:
        ordering = ['-person']