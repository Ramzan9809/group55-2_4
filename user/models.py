from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator 

class Profile(models.Model):
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0) 
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
