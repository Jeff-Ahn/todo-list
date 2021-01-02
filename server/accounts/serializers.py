from rest_framework import serializers
from .models import Account


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password']