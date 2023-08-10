# Generated by Django 4.2.3 on 2023-08-04 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_task_cancel_time_alter_task_closed_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_time']},
        ),
        migrations.AlterField(
            model_name='guest',
            name='refused_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время отказа'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='visited_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время посещения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='cancel_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время отмены задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='closed_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время завершения задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(choices=[('MERCH', 'Выдать раздаточный материал')], default='MERCH', verbose_name='Описание задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='Мероприятие'),
        ),
        migrations.AlterField(
            model_name='task',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_task_set', to='events.guest', verbose_name='Гость'),
        ),
        migrations.AlterField(
            model_name='task',
            name='progress_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время взятия в работу'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PROGRESS', 'Задача в работе'), ('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача'), ('CANCEL', 'Задача отменена')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
