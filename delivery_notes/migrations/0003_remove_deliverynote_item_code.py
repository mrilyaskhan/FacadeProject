# Generated by Django 5.2.3 on 2025-07-05 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_notes', '0002_deliverynote_ref_number_deliverynote_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverynote',
            name='item_code',
        ),
    ]
