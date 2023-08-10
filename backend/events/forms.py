import datetime

from django import forms

from events import logger
from events.models import Event, Guest
from events.validators import guest_email_validator


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'start_date', 'end_date']

    start_time = forms.TimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'time',
        'value': '08:00'
    }), label='Начало мероприятия')

    start_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    end_time = forms.TimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'time',
        'value': '20:00'
    }), label='Окончание мероприятия')

    end_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if datetime.datetime.combine(start_date, start_time) > datetime.datetime.combine(end_date, end_time):
            msg = 'Начало мероприятия не может быть раньше конца мероприятия'
            self.add_error('start_date', msg)
            self.add_error('start_time', msg)


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['event']

class NewGuestForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email'
    }), label='Адрес электронной почты')

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text'
    }), label='Имя')

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text'
    }), label='Фамилия')


class ExistingGuestForm(forms.Form):
    send_alert = forms.BooleanField(label='Отправить уведомление пользователю', required=False)


class SetVisitedConfirmForm(forms.Form):
    dont_create_task = forms.BooleanField(label='Не создавать задание для организаторов', required=False)