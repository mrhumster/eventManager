# Generated by Django 4.2.4 on 2023-08-07 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CANCEL', 'Задача отменена'), ('PROGRESS', 'Задача в работе'), ('CLOSED', 'Задача завершена'), ('NEW', 'Новая задача')], default='NEW', verbose_name='Статус задачи'),
        ),
    ]