from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    item = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.item} - {self.quantity}"

class Step(models.Model):
    image = models.URLField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.description

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    cooking_time = models.CharField(max_length=50)
    equipment = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    steps = models.ManyToManyField(Step)

    def __str__(self):
        return self.title
