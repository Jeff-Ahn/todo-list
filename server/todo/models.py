from django.db import models
from account.models import User


class Todo(models.Model):
    content = models.TextField()
    is_done = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        related_name="todos",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.content
