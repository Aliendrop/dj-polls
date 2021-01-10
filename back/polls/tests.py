from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

from .models import Poll, Question


class PollsAppModelsTest(TestCase):
    poll_title = 'Awesome poll!'
    poll_desc = 'Some poll description.'
    question_text = 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia'

    @classmethod
    def setUpTestData(cls):
        cls.current_dt = timezone.localtime(timezone.now())
        cls.the_poll = Poll.objects.create(
            title=cls.poll_title,
            description=cls.poll_desc,
            start_at=timezone.localtime(timezone.now()),
            end_at=timezone.localtime(timezone.now()) + timedelta(days=3),
        )
        cls.the_question = Question.objects.create(
            poll=cls.the_poll,
            text=cls.question_text,
            question_type=Question.AS_TEXT
        )

    def setUp(self):
        pass

    def test_poll_content(self):
        poll = Poll.objects.get(pk=1)

        self.assertEqual(poll.title, self.poll_title)
        self.assertEqual(poll.description, self.poll_desc)
        self.assertEqual(poll.start_at.date(), self.current_dt.date())
        self.assertEqual(poll.end_at.date(), self.current_dt.date() + timedelta(days=3))

    def test_question_content(self):
        question = Question.objects.get(pk=1)

        self.assertEqual(question.poll.pk, self.the_poll.pk)
        self.assertEqual(question.question_type, Question.AS_TEXT)
        self.assertEqual(question.text, self.question_text)
