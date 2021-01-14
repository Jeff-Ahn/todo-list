from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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
        return Response(status.HTTP_200_OK)
