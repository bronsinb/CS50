# Generated by Django 3.0.8 on 2020-09-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='image',
            field=models.CharField(default='https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png', max_length=2000),
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.CharField(default='https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png', max_length=2000),
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=8),
            preserve_default=False,
        ),
    ]