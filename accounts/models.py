from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default-avatar.png', blank=True, null=True)
    # other fields...
    
    def __str__(self):
        return self.user.username
