# Generated by Django 5.2.3 on 2025-07-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverynote',
            name='ref_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=20),
        ),
    ]
