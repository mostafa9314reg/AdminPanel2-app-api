"""
Here we creating tests for user api in our TDD process
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status



CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')



def create_user(**kwargs):
    """creating new users"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()


    def test_create_user_success(self):
        """Test creating a user is successful."""

        user_info ={
            'email' : '123@example.com',
            'password' : '123pass',
            'name' : 'user1',
        }

        res = self.client.post(CREATE_USER_URL,user_info)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=user_info['email'])
        self.assertTrue(user.check_password(user_info['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exist_error_bad_request(self):
        """test error returns if user with same email exist in creation process"""
        user_info = {
            'email' : '123@example.com',
            'password' : '123pass',
            'name' : 'user1',
        }
        create_user(**user_info)
        res = self.client.post(CREATE_USER_URL,user_info)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """test an error is returned if password less than 6 chars"""
        user_info = {
            'email' : '123@example.com',
            'password' : '123p',
            'name' : 'user1',
        }
        res = self.client.post(CREATE_USER_URL,user_info)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=user_info['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """test create token for created user"""
        user_detail = {
            'email' : 'test@example.com',
            'password' : 'pass1234',
            'name' : 'usertest'
        }
        payload = {
            'email' : user_detail['email'],
            'password' : user_detail['password']
        }

        create_user(**user_detail)
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """test bad credential if user password was wrong"""

        user_info={
            'email' : 'email@example.com',
            'password' : '123pass',
            'name' : 'mostafa',
        }

        payload = {
            'email' : 'mostafa@mail.com',
            'password' : 'pass123',
        }
        create_user(**user_info)
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """test error returnd if user not found for given email"""

        payload = {
            'email' : '123@mostafa.com',
            'password' : '123pass',
        }

        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """test returnd error if user password was blank"""

        payload = {
            'email' : '123@example.com',
            'password' : '',
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)