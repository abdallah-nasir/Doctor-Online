# Generated by Django 3.2.4 on 2021-09-12 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_place_point'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='city',
            new_name='lat_lng',
        ),
    ]
