import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class SomeUser(AbstractUser):
    img = models.ImageField(null=True, upload_to='static/img/')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='static/img/')
    pub_date = models.DateTimeField('date published')
    voted_users = models.ManyToManyField(SomeUser, null=True, blank=True, verbose_name='Проголосовавшие',
                                         related_name='related_user')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
