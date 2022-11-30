from django.test import TestCase
from user.models import UserAccount


class UserTestCase(TestCase):

    def setUp(self):
        self.user1 = UserAccount.objects.create(
            first_name='1234567890',
            last_name='0987654321',
            email='email@email.com',
            summary='Some summary'
        )

    def test_user_validity_with_good_input(self):
        user = self.user1
        self.assertEqual(user.first_name, '1234567890')
        self.assertEqual(user.last_name, '0987654321')
        self.assertEqual(user.email, 'email@email.com')
        self.assertEqual(user.summary, 'Some summary')
        self.assertEqual(user.role, 'user')

    def test_user_already_exist(self):
        with self.assertRaises(Exception):
            UserAccount.objects.create(
                first_name='1234567890',
                last_name='0987654321',
                email='email@email.com',
                summary='Some summary'
            )
