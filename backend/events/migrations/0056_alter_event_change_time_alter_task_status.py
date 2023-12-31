# Generated by Django 4.2.4 on 2023-08-09 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0055_guest_image_alter_event_change_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='change_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 9, 10, 16, 17, 824463, tzinfo=datetime.timezone.utc), verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача'), ('CANCEL', 'Задача отменена'), ('PROGRESS', 'Задача в работе')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
