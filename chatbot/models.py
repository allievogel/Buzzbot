from __future__ import unicode_literals

# Create your models here.
from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name

class Answer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    objective = models.CharField(max_length=200)
    audience = models.CharField(max_length=200)
    timeline = models.CharField(max_length=200)
    format = models.CharField(max_length=200)
    concept = models.CharField(max_length=200)
    detail = models.CharField(max_length=200)
    feeling = models.CharField(max_length=200)
    schedule = models.CharField(max_length=200)



    def __str__(self):
        return self.objective




