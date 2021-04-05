from django.db import models
from django.contrib.auth.models import User


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
