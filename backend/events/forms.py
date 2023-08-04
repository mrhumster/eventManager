from django import forms

from events.models import Event, Guest
from events.validators import guest_email_validator


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'start_date', 'end_date']

    start_time = forms.TimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }), label='Начало мероприятия')

    start_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    end_time = forms.TimeField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }), label='Окончание мероприятия')

    end_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))


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