# # Create your models here.

from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from django.utils.text import slugify
# from voting.models import VoteManager
# # from voting.models import get_score


# class Question(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
#     title = models.CharField(max_length=255)
#     slug = AutoSlugField(populate_from='title', unique=True)
#     detail = models.TextField()
#     tags = TaggableManager()  # Taggit field

#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.title    
    
#     objects = models.Manager()
#     votes = VoteManager()              

#     @property
#     def score(self):
#         return self.votes.get_score()['score']

# class Answer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
#     detail = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     votes = VoteManager()

#     @property
#     def score(self):
#         return self.votes.get_score()['score']


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    detail = models.TextField()
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def score(self):
        return Vote.objects.get_score(self)['score']


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def score(self):
        return Vote.objects.get_score(self)['score']
