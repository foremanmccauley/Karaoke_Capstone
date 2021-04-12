# Generated by Django 3.1.7 on 2021-04-10 21:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('karaoke', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='newAccount',
        ),
        migrations.AddField(
            model_name='profile',
            name='group',
            field=models.ManyToManyField(blank=True, related_name='group_set', to='karaoke.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_group_parent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends_set', to='karaoke.Profile'),
        ),
        migrations.CreateModel(
            name='GroupRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user_grp', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_grp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
