# Generated by Django 3.0.8 on 2020-08-29 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20200829_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follower',
        ),
    ]
