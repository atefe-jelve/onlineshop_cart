from rest_framework import serializers
from .models import BaseUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('username', 'phone_number', 'password')

        extra_kwargs = {
            'password' : {'write_only': True},
        }
