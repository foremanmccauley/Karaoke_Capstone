from django.db import models

class MP3(models.Model):
    title = models.CharField(max_length=250)
    song = models.FileField()

    def __str__(self):
        return self.title