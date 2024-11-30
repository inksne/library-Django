from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Book


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': False}
        }


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user