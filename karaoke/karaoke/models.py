from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mimetypes import guess_type


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('Profile', related_name = "friends_set", blank=True)
    group = models.ManyToManyField('Profile', related_name = "group_set", blank=True)
    is_group_parent = models.BooleanField(default=True)
    mp3name = models.CharField(max_length=100, blank=True)
    mp4name = models.CharField(max_length=100, blank=True) 
    
    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user=models.ForeignKey(User, related_name="from_user",on_delete=models.CASCADE)
    to_user=models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.from_user.username + " to " + self.to_user.username

class GroupRequest(models.Model):
    from_user=models.ForeignKey(User, related_name="from_user_grp",on_delete=models.CASCADE)
    to_user=models.ForeignKey(User, related_name='to_user_grp', on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.from_user.username + " to " + self.to_user.username

class MP3(models.Model):
    def validate_audio_file(val):
        if 'audio' not in val.content_type:
            raise ValidationError('Please only audio files please!')

    title = models.CharField(max_length=250)
    song = models.FileField(validators=[validate_audio_file])

    def __str__(self):
        return self.title

class MP4(models.Model):
    def validate_video_file(val):
        if 'video' not in val.content_type:
            raise ValidationError('Please only video files please!')

    title = models.CharField(max_length=250)
    video = models.FileField(validators=[validate_video_file])

    def __str__(self):
        return self.title
