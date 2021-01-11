from django.db.models.query_utils import Q
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

from polls.models import Poll, Question
from .common import CommonTest, DEFAULT_PASSWORD


def _get_polls_data(val=0) -> dict:
    return {
        "title": f"test-{val}",
        "description": f"test description-{val}",
        "start_at": f"2021-0{val}-08T19:00:00.000000Z",
        "end_at": f"2021-0{val}-10T18:00:00.000000Z"
    }

def _get_questions_data(val=0) -> dict:
    return {
        "text": f"test-question-{val}",
        "question_type": Question.SELECT_MULTIPLE
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

    def test_crud_questions(self):
        self._do_login(self.the_staff_user)

        # Add poll with question
        tmp_data = _get_polls_data(val=1)
        tmp_data['questions'] = [_get_questions_data()]
        response = self.client.post(
            reverse('polls-list'),
            data=json.dumps(tmp_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        poll = Poll.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        self.assertEqual(question.poll.pk, poll.pk)

        # Add question to poll
        new_question_data = _get_questions_data(val=1)
        response = self.client.post(
            reverse('polls-question', args=[poll.pk]),
            data=json.dumps(new_question_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_question = Question.objects.get(pk=2)
        self.assertEqual(new_question.poll.pk, poll.pk)

        # Delete question
        response = self.client.delete(
            '{}{}/'.format(reverse('polls-question', args=[poll.pk]), new_question.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.all().count(), 1)

        # Patch question
        self.assertEqual(question.question_type, Question.SELECT_MULTIPLE)
        question_patch_data = {
            'question_type': Question.SELECT
        }
        response = self.client.patch(
            '{}{}/'.format(reverse('polls-question', args=[poll.pk]), question.pk),
            data=json.dumps(question_patch_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Question.objects.get(pk=1).question_type, Question.SELECT)

        # Put question
        response = self.client.put(
            '{}{}/'.format(reverse('polls-question', args=[poll.pk]), question.pk),
            data=json.dumps(_get_questions_data(val=77)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        modified_question = Question.objects.get(pk=question.pk)
        self.assertEqual(modified_question.question_type, Question.SELECT_MULTIPLE)
        self.assertTrue('77' in modified_question.text)
