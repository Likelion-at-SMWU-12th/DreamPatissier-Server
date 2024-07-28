from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}의 유형은 {self.result_id}"