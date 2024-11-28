from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Book

class BookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Book
        fields = ['id', 'user', 'name', 'author', 'publisher', 'description', 'content', 'language']


class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    # password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': False}
        }

    # def validate(self, data):
    #     if data['password'] != data['password_confirm']:
    #         raise serializers.ValidationError({"password": "Пароли не совпадают"})
    #     print(data)
    #     return data

    def create(self, validated_data):
        # validated_data.pop('password_confirm') 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user