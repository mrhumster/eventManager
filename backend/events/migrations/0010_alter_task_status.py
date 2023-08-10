# Generated by Django 4.2.4 on 2023-08-04 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PROGRESS', 'Задача в работе'), ('CANCEL', 'Задача отменена'), ('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
