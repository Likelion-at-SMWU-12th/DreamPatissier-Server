from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Recipe(models.Model):
    title= models.CharField(max_length=255)
    image=models.ImageField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255)
    cookingTime = models.CharField(max_length=255)
    equipment = models.CharField(max_length=100)
    ingredients = models.JSONField(default=list, blank=True, null=True)
    step1_image = models.ImageField(blank=True, null=True)
    step1_description = models.TextField(blank=True, null=True)
    step2_image = models.ImageField(blank=True, null=True)
    step2_description = models.TextField(blank=True, null=True)
    step3_image = models.ImageField(blank=True, null=True)
    step3_description = models.TextField(blank=True, null=True)
    step4_image = models.ImageField(blank=True, null=True)
    step4_description = models.TextField(blank=True, null=True)
    step5_image = models.ImageField(blank=True, null=True)
    step5_description = models.TextField(blank=True, null=True)
    step6_image = models.ImageField(blank=True, null=True)
    step6_description = models.TextField(blank=True, null=True)
    step7_image = models.ImageField(blank=True, null=True)
    step7_description = models.TextField(blank=True, null=True)
    step8_image = models.ImageField(blank=True, null=True)
    step8_description = models.TextField(blank=True, null=True)
    step9_image = models.ImageField(blank=True, null=True)
    step9_description = models.TextField(blank=True, null=True)
    step10_image = models.ImageField(blank=True, null=True)
    step10_description = models.TextField(blank=True, null=True)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'bookmarks')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} bookmarked {self.recipe.title}'