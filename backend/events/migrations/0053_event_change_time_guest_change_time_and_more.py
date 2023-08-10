# Generated by Django 4.2.4 on 2023-08-09 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0052_task_change_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='change_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Время изменения'),
        ),
        migrations.AddField(
            model_name='guest',
            name='change_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача'), ('PROGRESS', 'Задача в работе'), ('CANCEL', 'Задача отменена')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]