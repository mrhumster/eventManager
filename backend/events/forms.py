from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from events.models import Event, Guest
from django.forms.widgets import MultiWidget, SplitDateTimeWidget


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