# Generated by Django 4.2.4 on 2023-08-07 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новая задача'), ('CANCEL', 'Задача отменена'), ('CLOSED', 'Задача завершена'), ('PROGRESS', 'Задача в работе')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]
