""" url maping for sip API"""

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from sip import views

router = DefaultRouter()
router2 = DefaultRouter()
router.register(r'accounts', views.SipVeiwSet)
# router2.register(r'create', views.SipCreateVeiwSet)

app_name = 'sip'

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(router2.urls))

]