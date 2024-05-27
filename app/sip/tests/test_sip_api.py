"""Here we create test for sip API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Accounts
from sip.serializers import SipSerializer


ACCOUNTS_URL = reverse('account:accounts_list')

def create_sip_account(**params):
        """create  sip account with params"""
        defult ={
            'pcode' : 1234,
            'extension' : '4321',
            'callerid' : 'test1',
            'mailbox' : 'test@example.com',
            'level' : 'test',
            'secret' : 'test1234',
            'server' : 'testserv',
            'enable' : 1,
        }
        defult.update(**params)
        account = Accounts.objects.create(**defult)
        return account

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicAccountApiTests(TestCase):
        """writing test for unauthenticated user"""


        def setUp(self) -> None:
                self.client = APIClient()

        def test_unauthorized_user_error(self):
                """test for unauthorized user cant access sip accounts list"""
                res = self.client.get(ACCOUNTS_URL)
                self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateAccountApiTests(TestCase) :
        """writing tests for authenticated user on retreiving sip accounts list"""
        def setUp(self) -> None:
                self.client = APIClient()
                user =create_user(
                       email = 'test@example.com',
                       password = 'testpass'
                )
                self.user = self.client.force_authenticate(self.user)
                self.account = create_sip_account()

        def test_retreive_account_listsr(self):
               """ test authenticated user can retreive accounts list"""
               create_sip_account()
               create_sip_account()
               account = Accounts.objects.all().order_by('-id')
               serializer = SipSerializer(account, many = True)
               res = self.client.get(ACCOUNTS_URL)
               self.assertEqual(res.status_code,status.HTTP_200_OK)
               self.assertEqual(res.data , serializer.data)








