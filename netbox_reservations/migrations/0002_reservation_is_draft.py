# Generated by Django 4.1.5 on 2023-02-03 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_draft',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]