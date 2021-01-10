from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(
        methods=['patch'],
        detail=True,
    )
    def change_password(self, request, pk):
        user = self.get_object()
        new_password = request.data['password']
        user.set_password(new_password)
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        methods=['patch'],
        detail=True,
    )
    def change_name(self, request, pk):
        user = self.get_object()
        new_username = request.data['username']
        user.set_username(new_username)
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
