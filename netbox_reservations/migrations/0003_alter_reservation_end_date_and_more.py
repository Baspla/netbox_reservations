# Generated by Django 4.1.5 on 2023-02-07 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_reservations', '0002_reservation_is_draft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
