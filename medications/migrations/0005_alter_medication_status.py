# Generated by Django 5.1.1 on 2024-10-09 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0004_alter_medication_status_alter_medication_total_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], default='active', max_length=50),
        ),
    ]