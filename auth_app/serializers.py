from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'name']

class SocialSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True,)
    last_name = serializers.CharField(required=True,)
    email = serializers.EmailField(required=True, )
    mode = serializers.CharField(required=True,)

class TokenValidateSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=20)