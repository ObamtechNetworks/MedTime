# Generated by Django 5.1.1 on 2024-10-11 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0009_rename_last_intake_time_medication_last_scheduled_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='last_scheduled_time',
        ),
    ]
