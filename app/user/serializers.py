"""Creating Serializers for User API View"""



from django.contrib.auth import get_user_model

from rest_framework import serializers



class  UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}


    def create(self,validated_data):
        """overide user object creation to add password encryption"""
        return get_user_model().objects.create_user(**validated_data)