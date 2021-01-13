from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all(),
                                           message="이미 동일한 이메일 주소로 가입되어 있습니다.")
                                   ])
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     max_length=128)

    def create(self, validated_data):
        return User.objects.create_user(email=validated_data['email'],
                                        username=validated_data['username'],
                                        password=validated_data['password'])

    def update(self, instance, validated_data):
        raise NotImplementedError('잘못된 요청입니다.')

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
