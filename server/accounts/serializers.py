from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Person


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all(),
                                           message="이미 동일한 이메일 주소로 가입되어 있습니다.")
                                   ])
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     max_length=128)

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

    def update(self, instance, validated_data):
        raise NotImplementedError('잘못된 요청입니다.')

    class Meta:
        model = User
        fields = ['email', 'password']


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)

        user = User.objects.create_user(email=user_data['email'], password=user_data['password'])
        person = Person.objects.create(user=user, **validated_data)
        return person

    def update(self, instance, validated_data):
        validated_data.pop('user', None)

        return super(PersonSerializer, self).update(instance, validated_data)

    def validate(self, attrs):
        if not attrs['first_name'] or \
                not attrs['last_name'] or \
                not attrs['user']['email']:
            raise ValueError('필수 정보를 입력하세요.')
        return attrs

    class Meta:
        model = Person
        fields = ['user', 'first_name', 'last_name', 'nickname', 'sex']


class SignUpPersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        person = Person.objects.create(**validated_data)

        return person

    class Meta:
        model = Person
        fields = ['user', 'first_name', 'last_name']
