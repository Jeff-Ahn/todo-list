from rest_framework.permissions import IsAuthenticated

from .serializers import TodoSerializers
from .permissions import IsOwnerForTodo
from rest_framework import viewsets


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerForTodo]
    serializer_class = TodoSerializers

    def get_queryset(self):
        return self.request.user.todos.all()
