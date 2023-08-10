# Generated by Django 4.2.4 on 2023-08-07 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0036_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_task_set', to='events.guest', verbose_name='Исполнитель задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CLOSED', 'Задача завершена'), ('PROGRESS', 'Задача в работе'), ('CANCEL', 'Задача отменена'), ('NEW', 'Новая задача')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
