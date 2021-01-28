from rest_framework import viewsets
from .serializers import UserSerializer, PersonSerializer, SignUpPersonSerializer
from .models import Person
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout


class AccountViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        print('data:', data)

        user = self._create_user(data)
        person = self._create_person(data['first_name'], data['last_name'], user)
        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=['PATCH'],
        url_name='change-password',
        url_path='password',
        detail=False,
    )
    def change_password(self, request):
        user = request.user
        new_password = request.data['password']
        user.set_password(new_password)
        user.save()
        return Response(status.HTTP_200_OK)

    def _create_user(self, data):
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid(raise_exception=True):
            return user_serializer.save()

    def _create_person(self, first_name, last_name, user):
        person_data = {
            'user': user.pk,
            'first_name': first_name,
            'last_name': last_name
        }
        signup_person_serializer = SignUpPersonSerializer(data=person_data)
        if signup_person_serializer.is_valid(raise_exception=True):
            return signup_person_serializer.save()

    # @action(
    #     methods=['PATCH'],
    #     url_name='change-username',
    #     url_path='username',
    #     detail=False,
    # )
    # def change_name(self, request):
    #     user = request.user
    #     new_username = request.data['username']
    #     user.set_username(new_username)
    #     user.save()
    #     return Response(status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data

        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            raise ValidationError('이메일과 패스워드를 확인하세요.')

        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError('가입하지 않은 이메일이거나, 잘못된 비밀번호 입니다.')

        if user.is_active:
            login(request, user)
            return Response(status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.select_related('user')

    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)
