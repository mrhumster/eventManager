# Generated by Django 4.2.4 on 2023-08-07 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PROGRESS', 'Задача в работе'), ('CLOSED', 'Задача завершена'), ('CANCEL', 'Задача отменена'), ('NEW', 'Новая задача')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
