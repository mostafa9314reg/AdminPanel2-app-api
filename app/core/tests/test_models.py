"""
Tests for models
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """
    Test Models
    """

    def test_create_user_with_email_successful(self):
        """
        Tests creating user with email is successful
        """
        email = 'test@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError)  :
            user = get_user_model().objects.create_user('','sample123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
             'test@example.com',
             'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_creat_account(self):
        account = models.Accounts.objects.create(
            pcode = 1234,
            extension = '4321',
            callerid = 'test1',
            mailbox = 'test@example.com',
            level = 'test',
            secret = 'test1234',
            server = 'testserv',
            enable = 1

        )
        self.assertEqual(str(account),account.extension)