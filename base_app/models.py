from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='messages')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.owner}: {self.content[:50]}"
