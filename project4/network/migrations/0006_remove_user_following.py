# Generated by Django 3.0.8 on 2020-08-28 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20200828_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
    ]
