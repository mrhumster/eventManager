# Generated by Django 4.2.4 on 2023-08-08 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0040_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача'), ('CANCEL', 'Задача отменена'), ('PROGRESS', 'Задача в работе')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]