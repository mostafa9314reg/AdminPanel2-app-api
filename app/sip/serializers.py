"""Creating serializers for Sip Api Veiw"""

from rest_framework import serializers
from core.models import Accounts


class SipSerializer(serializers.ModelSerializer):
    """Serializer for sip account objects"""
    class Meta:
        model = Accounts
        # fields = "__all__"
        fields = [
            'id','pcode','extension','secret','callerid','mailbox',
            'zones','level','groups','cfwd','regione','server','enable','lastupdate']
        read_only_fields = ['id']
class SipDetailSerializer(SipSerializer):
    """serializer for sip account detail"""

    class Meta(SipSerializer.Meta):
        fields = SipSerializer.Meta.fields + ['extension']
        # fields = SipSerializer.Meta.fields + ['description']


class SipCreateSerializer(SipSerializer):
    """serializer for creating sip account"""


    def validate_mailbox(self,value):
        """validate if email exist rais error"""
        # email = attrs['mailbox']
        if Accounts.objects.filter(mailbox = value).exists() :
            raise serializers.ValidationError("Duplicate Email Entry")
        return value

    class Meta(SipSerializer.Meta):
        # fields = SipSerializer.Meta.fields
         extra_kwargs = {'secret': { 'write_only': True,'min_length': 6}}









