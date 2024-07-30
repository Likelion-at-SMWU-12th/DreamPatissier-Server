from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    item = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.item} - {self.quantity}"

class Step(models.Model):
    image = models.ImageField(null=True, blank=True) #URLField에서 ImageField로 수정
    description = models.TextField()

    def __str__(self):
        return self.description

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True) #URLField에서 ImageField로 수정
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    cookingTime = models.CharField(max_length=50)
    equipment = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    steps = models.ManyToManyField(Step)

    def __str__(self):
        return self.title
    
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'bookmarks')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} bookmarked {self.recipe.title}'