# Generated by Django 3.0.8 on 2020-09-14 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_book'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Book',
            new_name='Booking',
        ),
    ]