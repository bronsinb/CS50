# Generated by Django 3.0.8 on 2020-09-16 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_card_expire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='card',
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='card', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
