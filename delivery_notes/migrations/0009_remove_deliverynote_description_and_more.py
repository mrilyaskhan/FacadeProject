# Generated by Django 5.2.3 on 2025-07-08 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_notes', '0008_remove_deliverynote_total_remarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverynote',
            name='description',
        ),
        migrations.RemoveField(
            model_name='deliverynote',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='deliverynote',
            name='so_number',
        ),
        migrations.RemoveField(
            model_name='deliverynote',
            name='unit',
        ),
        migrations.AddField(
            model_name='deliveryitem',
            name='so_number',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
