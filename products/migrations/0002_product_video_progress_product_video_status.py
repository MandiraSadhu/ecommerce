# Generated by Django 5.0.8 on 2024-08-10 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='video_progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='video_status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]
