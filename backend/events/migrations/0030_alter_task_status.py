# Generated by Django 4.2.4 on 2023-08-07 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CLOSED', 'Задача завершена'), ('CANCEL', 'Задача отменена'), ('PROGRESS', 'Задача в работе'), ('NEW', 'Новая задача')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
