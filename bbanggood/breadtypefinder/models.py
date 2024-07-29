from django.db import models
from django.contrib.auth import get_user_model
from bakery.models import Bread

# Create your models here.
User = get_user_model()

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_id = models.PositiveIntegerField()
    result_type = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}의 유형은 {self.result_id}번 {self.result_type}입니다."
    

'''class ResultType(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    description1 = models.TextField(blank=True, null=True)
    description2 = models.TextField(blank=True, null=True)
    description3 = models.TextField(blank=True, null=True)'''