# Generated by Django 4.1.6 on 2023-02-10 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_reservations', '0003_alter_reservation_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='is_draft',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateField(),
        ),
    ]