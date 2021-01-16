from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

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

    @action(
        methods=['PATCH'],
        url_name='change-username',
        url_path='username',
        detail=False,
    )
    def change_name(self, request):
        user = request.user
        new_username = request.data['username']
        user.set_username(new_username)
        user.save()
        return Response(status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data

        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            raise ValidationError('이메일과 패스워드를 확인하세요.')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)