# Generated by Django 3.0.8 on 2020-09-12 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]