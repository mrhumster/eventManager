# Generated by Django 4.2.3 on 2023-08-02 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_end_date_event_start_date_alter_event_end_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date']},
        ),
    ]
