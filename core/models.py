# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=20)  # admin, editor, user

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.role.name if self.role else 'No Role'}"
 

