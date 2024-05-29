""""Here we create some veiws for sip api"""

from .serializers import SipSerializer
from rest_framework import viewsets,generics,permissions,authentication
from core.models import Accounts


class SipVeiwSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = SipSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

