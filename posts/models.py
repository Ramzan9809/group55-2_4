from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    img = models.ImageField(upload_to='media/', null=True)
    content = models.CharField(max_length=256, null=True)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title