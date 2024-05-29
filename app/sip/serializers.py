"""Creating serializers for Sip Api Veiw"""

from rest_framework import serializers
from core.models import Accounts


class SipSerializer(serializers.ModelSerializer):
    """Serializer for sip account objects"""
    class Meta:
        model = Accounts
        fields = "__all__"
