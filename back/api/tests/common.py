from django.contrib.auth import get_user_model
from django.test.testcases import TestCase


CLIENT_USERNAME = 'uclient'
STAFF_USERNAME = 'ustaff'
DEFAULT_PASSWORD = 'ManaMana!'


class CommonTest(TestCase):
    """ Initial with dummy users """
    @classmethod
    def setUpTestData(cls):
        cls.the_client_user = create_test_user(username=CLIENT_USERNAME)
        cls.the_staff_user = create_test_user(username=STAFF_USERNAME, is_staff=True)

    def setUp(self):
        pass


def create_test_user(username, is_staff=False, is_superuser=False):
    return get_user_model().objects.create_user(
        first_name="Test",
        last_name="User",
        email="test_user@test.com",
        username=username,
        password=DEFAULT_PASSWORD,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
