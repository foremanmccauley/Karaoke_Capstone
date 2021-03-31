from django.db import models
from django.core.exceptions import ValidationError
from mimetypes import guess_type

class MP3(models.Model):
    def validate_audio_file(val):
        if 'audio' not in val.content_type:
            raise ValidationError('Please only audio files please!')

    title = models.CharField(max_length=250)
    song = models.FileField(validators=[validate_audio_file])

    def __str__(self):
        return self.title