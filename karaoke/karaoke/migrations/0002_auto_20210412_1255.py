# Generated by Django 3.1.7 on 2021-04-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mp3name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='mp4name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
