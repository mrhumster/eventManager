# Generated by Django 4.2.3 on 2023-08-04 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='cancel_time',
            field=models.DateTimeField(null=True, verbose_name='Время отмены задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='closed_time',
            field=models.DateTimeField(null=True, verbose_name='Время завершения задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='progress_time',
            field=models.DateTimeField(null=True, verbose_name='Время взятия в работу'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CANCEL', 'Задача отменена'), ('NEW', 'Новая задача'), ('PROGRESS', 'Задача в работе'), ('CLOSED', 'Задача завершена')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
