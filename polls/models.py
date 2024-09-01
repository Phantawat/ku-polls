import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    A Question model class contains question attributes
    and a method for checking is question published
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
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

    def is_published(self):
        """
        returns True if the current date-time is on
        or after question’s publication date.
        """
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """
        returns True if voting is allowed for this question.
        """
        if self.end_date:
            return self.pub_date <= timezone.now() <= self.end_date
        return self.pub_date <= timezone.now()


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
