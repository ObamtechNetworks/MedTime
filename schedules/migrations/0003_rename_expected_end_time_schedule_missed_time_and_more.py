# Generated by Django 5.1.1 on 2024-10-09 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_rename_next_dose_schedule_next_dose_schedule_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='expected_end_time',
            new_name='missed_time',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='start_time',
            new_name='schedule_time',
        ),
    ]
