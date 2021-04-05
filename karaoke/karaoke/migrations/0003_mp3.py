# Generated by Django 3.1.7 on 2021-03-30 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0002_remove_spotifytoken_refresh_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='MP3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('song', models.FileField(upload_to='songs/%Y/%m/%d')),
            ],
        ),
    ]
