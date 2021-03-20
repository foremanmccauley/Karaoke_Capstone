from django.db import models

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()