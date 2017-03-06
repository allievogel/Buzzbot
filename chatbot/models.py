from __future__ import unicode_literals


# Create your models here.
from django.db import models

class Questions(models.Model):
    question_ID = models.IntegerField(default=0)
    keyword_goal = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword_goal

class Options(models.Model):
    question_ID = models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_ID

class Users(models.Model):
    user_name = models.CharField(max_length=200)
    set_cookie = models.IntegerField(default=0)

    def __str__(self):
        return self.user_name



