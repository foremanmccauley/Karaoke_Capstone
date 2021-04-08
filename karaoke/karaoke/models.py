from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mimetypes import guess_type


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('Profile', blank=True)
    newAccount = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user=models.ForeignKey(User, related_name="from_user",on_delete=models.CASCADE)
    to_user=models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
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
