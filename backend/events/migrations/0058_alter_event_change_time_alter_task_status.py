# Generated by Django 4.2.15 on 2024-08-21 04:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0057_alter_event_change_time_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='change_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 21, 4, 39, 42, 654581, tzinfo=datetime.timezone.utc), verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CANCEL', 'Задача отменена'), ('PROGRESS', 'Задача в работе'), ('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
