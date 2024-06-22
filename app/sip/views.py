""""Here we create some veiws for sip api"""

from .serializers import SipSerializer,SipDetailSerializer,SipCreateSerializer
from rest_framework import viewsets,generics,permissions,authentication
from core.models import Accounts


class SipVeiwSet(viewsets.ModelViewSet):
    """view to manage sip api"""
    queryset = Accounts.objects.all()
    serializer_class = SipDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """returns serializer class per action"""

        if self.action == 'list':
            return SipSerializer

        elif self.action == 'create':
            return SipCreateSerializer

        return self.serializer_class

    # def perform_create(self,serializer):
        # """saving serializer object"""
        # serializer.save()



# class SipCreateVeiwSet(viewsets.ModelViewSet):
#     """view to manage sip api"""
#     queryset = Accounts.objects.all()
#     serializer_class = SipCreateSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self,serializer):
        ...




