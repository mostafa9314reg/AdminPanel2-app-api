""" url maping for sip API"""

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from sip import views

router = DefaultRouter()
router.register(r'accounts', views.SipVeiwSet)

app_name = 'sip'

urlpatterns = [
    path('', include(router.urls)),
]