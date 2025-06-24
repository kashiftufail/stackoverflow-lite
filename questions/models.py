# Create your models here.

from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    detail = models.TextField()
    tags = TaggableManager()  # Taggit field

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    


