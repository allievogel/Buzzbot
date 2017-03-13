from __future__ import unicode_literals


# Create your models here.
from django.db import models


class Users(models.Model):
    user_name = models.CharField(max_length=200)
    set_cookie = models.IntegerField(default=0)
    session_id = models.IntegerField(default=0)

    def __str__(self):
        return self.user_name


class Brief(models.Model):
    brief_type = models.CharField(max_length=200)

    def __str__(self):
        return self.brief_type


#class Questions(models.Model):
    #question_ID = models.IntegerField(default=0)
    #keyword_goal = models.CharField(max_length=200)
    #question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword_goal

#class Answers(models.Model):
    #question_ID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    #answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_ID, #self.answer_text




