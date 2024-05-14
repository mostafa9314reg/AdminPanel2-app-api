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
ME_URL = reverse('user:me')



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

    def test_retrieve_me_unautheticated_error(self):
        """tests return error if unauthenticated user retrives me"""
        res=self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Tests autorized user api features"""

    def setUp(self):
        user_info = {
            'email': 'test@example.com',
            'password' : 'test123',
            'name' : 'testuser',
        }
        self.user = create_user(**user_info)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_me_authenticated_user_successful(self):
        """test if authnticated user retrive me endpoint"""
        res =self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_authenticated_user_post_me_error(self):
        """test returned error if user tries post request on me endpoint"""
        payload = {}
        res = self.client.post(ME_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticated_user_change_info_me(self):
        """test if authenticated user can change user info in me endpoint"""

        payload = {'name': 'Updated name', 'password': 'newpassword123' }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
