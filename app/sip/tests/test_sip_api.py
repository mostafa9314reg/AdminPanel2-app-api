"""Here we create test for sip API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Accounts
from sip.serializers import (
    SipSerializer,
    SipDetailSerializer
)


ACCOUNTS_URL = reverse('sip:accounts-list')
# ACCOUNTS_CREATE_URL = reverse('sip:create')

def account_detail_url(account_id):

        return reverse('sip:accounts-detail',args=[account_id])

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
                self.user = create_user(
                       email = 'test@example.com',
                       password = 'testpass'
                )
                self.client.force_authenticate(self.user)
                self.account = create_sip_account()

        def test_retreive_account_listsr(self):
               """ test user can retreive accounts list"""
               create_sip_account(extension='6543')
               create_sip_account(extension = '9876')
        #        account = Accounts.objects.all().order_by('-id')
               account = Accounts.objects.all()
               serializer = SipSerializer(account, many = True)
               res = self.client.get(ACCOUNTS_URL)
               self.assertEqual(res.status_code,status.HTTP_200_OK)
               self.assertEqual(res.data , serializer.data)

        def test_retreive_account_detail(self):
                """ test user can see account detail"""
                account = create_sip_account(extension = '7654')
                serializer = SipDetailSerializer(account)
                detail_url = account_detail_url(account.id)
                res = self.client.get(detail_url)
                self.assertEqual(res.data,serializer.data)


        def test_create_account(self):
                """create sip acount api test"""
                payload ={
            'pcode' : 1334,
            'extension' : '5321',
            'callerid' : 'test1',
            'mailbox' : 'test7@example.com',
            'level' : 'test',
            'secret' : 'test1234',
            'server' : 'testserv',
            'enable' : 1,
        }
                res = self.client.post(ACCOUNTS_URL,payload)
                self.assertEqual(res.status_code,status.HTTP_201_CREATED)
                account = Accounts.objects.get(id=res.data['id'])
                for key,value in payload.items() :
                        self.assertEqual(getattr(account,key),value)

        def test_create_account_email_exist_error(self):
                """creat sip account withe duplicate email record error returns"""
                payload = {
            'pcode' : 1334,
            'extension' : '6543',
            'callerid' : 'test1',
            'mailbox' : 'test8@example.com',
            'level' : 'test',
            'secret' : 'test1234',
            'server' : 'testserv',
            'enable' : 1
                }
                create_sip_account(extension='5463',mailbox = 'test8@example.com')
                res = self.client.post(ACCOUNTS_URL,payload)
                account_exist = Accounts.objects.filter(mailbox = payload['extension']).exists()
                self.assertFalse(account_exist)
                self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        def test_create_account_secret_blank_bad_request_error(self):
                """test returns error if secret is blank in creation"""
                payload = {
            'pcode' : 1334,
            'extension' : '7543',
            'callerid' : 'test1',
            'mailbox' : 'test@example2.com',
            'level' : 'test',
            'secret' : '',
            'server' : 'testserv',
            'enable' : 1
                }
                res = self.client.post(ACCOUNTS_URL,payload)
                account_exist = Accounts.objects.filter(mailbox = payload['mailbox']).exists()
                self.assertFalse(account_exist)
                self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


        def test_create__account_too_short_secret_error(self):
                """test returns error if secret is too short"""
                payload = {
            'pcode' : 1334,
            'extension' : '8543',
            'callerid' : 'test1',
            'mailbox' : 'test@example2.com',
            'level' : 'test',
            'secret' : '123',
            'server' : 'testserv',
            'enable' : 1
                }
                res = self.client.post(ACCOUNTS_URL,payload)
                account_exist = Accounts.objects.filter(mailbox = payload['mailbox']).exists()
                self.assertFalse(account_exist)
                self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)






