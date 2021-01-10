from datetime import datetime
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

from .models import Poll


class PollModelTest(TestCase):
    poll_title = 'Awesome poll!'
    poll_desc = 'Some poll description.'

    def setUp(self):
        self.the_poll = Poll.objects.create(
            title=self.poll_title,
            description=self.poll_desc,
            start_at=timezone.now(),
            end_at=timezone.now() + timedelta(days=3),
        )

    def test_poll_content(self):
        current_dt = timezone.now()
        poll = Poll.objects.get(pk=1)

        self.assertEqual(poll.title, self.poll_title)
        self.assertEqual(poll.description, self.poll_desc)
        self.assertEqual(poll.start_at.date(), current_dt.date())
        self.assertEqual(poll.end_at.date(), current_dt.date() + timedelta(days=3))
