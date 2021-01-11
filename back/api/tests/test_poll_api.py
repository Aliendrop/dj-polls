from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

from polls.models import Poll
from .common import CommonTest, DEFAULT_PASSWORD


def _get_polls_data(val=0):
    return {
        "title": f"test-{val}",
        "description": f"test description-{val}",
        "start_at": f"2021-0{val}-08T19:00:00.000000Z",
        "end_at": f"2021-0{val}-10T18:00:00.000000Z"
    }


class PollApiTest(CommonTest, APITestCase):
    def _do_login(self, user):
        return self.client.login(
            username=user.username,
            password=DEFAULT_PASSWORD
        )

    def test_client_user_can_login(self):
        self.assertTrue(self._do_login(self.the_client_user))

    def test_staff_can_login(self):
        self.assertTrue(self._do_login(self.the_staff_user))

    def test_anon_user_get_polls(self):
        response = self.client.get(reverse('polls-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _create_polls(self, status_code, polls_count=5, expect_polls=0):
        for i in range(1, polls_count+1):
            tmp_data = _get_polls_data(val=i)
            response = self.client.post(
                reverse('polls-list'),
                data=json.dumps(tmp_data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status_code)
        created_count = Poll.objects.all().count()
        self.assertEqual(created_count, expect_polls)

    def test_diff_users_can_create_polls(self):
        self._create_polls(status.HTTP_403_FORBIDDEN)

        self._do_login(self.the_client_user)
        self._create_polls(status.HTTP_403_FORBIDDEN)

        self._do_login(self.the_staff_user)
        self._create_polls(status.HTTP_201_CREATED, polls_count=5, expect_polls=5)

    def test_staff_can_delete_polls(self):
        self._do_login(self.the_staff_user)
        self._create_polls(status.HTTP_201_CREATED, polls_count=1, expect_polls=1)

        response = self.client.delete(reverse('polls-detail', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        polls_count = Poll.objects.all().count()
        self.assertEqual(polls_count, 0)

    def test_staff_can_edit_polls_wo_start_date(self):
        self._do_login(self.the_staff_user)
        self._create_polls(status.HTTP_201_CREATED, polls_count=1, expect_polls=1)

        new_poll_data = _get_polls_data(val=7)

        response = self.client.patch(
            reverse('polls-detail', args=['1']),
            data=json.dumps(new_poll_data),
            content_type='application/json'
        )
        self.assertTrue('start_at' in response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_poll_data.pop('start_at')
        response = self.client.patch(
            reverse('polls-detail', args=['1']),
            data=json.dumps(new_poll_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        poll = Poll.objects.get(pk=1)
        self.assertTrue('7' in poll.title)
