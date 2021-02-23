from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .serializers import TodoSerializers
from .permissions import IsOwner
from account.models import User


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TodoSerializers

    def get_queryset(self):
        return self.request.user.todos.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        ownerId = data['owner']
        owner = User.objects.get(id=ownerId)

        if owner != user:
            raise PermissionDenied('다른 사용자의 todo를 생성할 수 없습니다.')

        return super().create(request, args, kwargs)
