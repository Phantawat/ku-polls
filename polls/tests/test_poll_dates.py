"""Tests of polls dates"""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published(self):
        """Test that is_published() returns True for questions whose publication date is in the past."""
        future_time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.is_published(), False)
        recent_time = timezone.now()
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.is_published(), True)
        past_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=past_time)
        self.assertIs(past_question.is_published(), True)

    def test_cannot_vote_after_end_date(self):
        """Cannot vote if the end_date is in the past."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        recent_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertIs(recent_question.can_vote(), False)

    def test_can_vote_before_end_date(self):
        """Can vote if the end_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=1)
        recent_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_without_end_date(self):
        """Can vote if there is no end_date set."""
        recent_question = Question(pub_date=timezone.now())
        self.assertIs(recent_question.can_vote(), True)
