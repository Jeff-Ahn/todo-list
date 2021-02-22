from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializers
from .permissions import IsOwner


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TodoSerializers

    def get_queryset(self):
        return self.request.user.todos.all()
