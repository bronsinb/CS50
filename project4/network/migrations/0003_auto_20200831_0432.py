# Generated by Django 3.0.8 on 2020-08-31 04:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20200831_0430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follower',
        ),
        migrations.AddField(
            model_name='user',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='_user_follower_+', to=settings.AUTH_USER_MODEL),
        ),
    ]