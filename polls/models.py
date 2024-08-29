import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    A Question model class contains question attributes
    and a method for checking is question published
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
        Return a question string.
        """
        return self.question_text

    def was_published_recently(self):
        """
        A method for checking is a question published.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    A Choice model class contains choice attributes
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Return a choice string.
        """
        return self.choice_text
