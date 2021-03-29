from rest_framework import serializers
from .models import Todo
from django.db import transaction


class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user

        todo = Todo.objects.create(
            owner=user,
            is_done=validated_data['is_done'],
            content=validated_data['content']
            )

        return todo