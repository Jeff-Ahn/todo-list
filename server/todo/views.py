from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .serializers import TodoSerializers
from .permissions import IsOwnerForTodo
from rest_framework.response import Response
from rest_framework import viewsets, status


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerForTodo]
    serializer_class = TodoSerializers

    def get_queryset(self):
        return self.request.user.todos.all()

    @transaction.atomic
    def create(self, request):
        data = request.data

        todo_serializer = TodoSerializers(data=data, context={'request': request})
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()

        return Response(None, status=status.HTTP_201_CREATED)
