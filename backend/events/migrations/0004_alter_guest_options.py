# Generated by Django 4.2.3 on 2023-08-03 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guest',
            options={'ordering': ['-person']},
        ),
    ]