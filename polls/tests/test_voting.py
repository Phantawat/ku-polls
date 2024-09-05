"""Tests of voting """
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionCanVoteTests(TestCase):
    """Tests for the can_vote method of the Question model."""

    def setUp(self):
        """Set up a Question."""
        self.future_start_date_question = Question.objects.create(
            question_text='Future start date question.',
            pub_date=timezone.now() + datetime.timedelta(days=5)
        )
        self.past_end_date_question = Question.objects.create(
            question_text='Past end date question.',
            pub_date=timezone.now() - datetime.timedelta(days=5),
            end_date=timezone.now() - datetime.timedelta(days=1)
        )
        self.published_question = Question.objects.create(
            question_text='Published question.',
            pub_date=timezone.now()
        )

    def test_can_vote_future_start_date(self):
        """ Tests that can_vote returns False
        when the start date is in the future. """
        self.assertFalse(self.future_start_date_question.can_vote())

    def test_can_vote_past_end_date(self):
        """ Tests that can_vote returns False
        when the end date is in the past. """
        self.assertFalse(self.past_end_date_question.can_vote())

    def test_can_vote_on_published_date(self):
        """ Tests that can_vote returns True when the start date is today. """
        self.assertTrue(self.published_question.can_vote())