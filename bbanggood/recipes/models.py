from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Ingredient(models.Model):
    item = models.CharField('재료명',max_length=100)
    quantity = models.CharField('수량',max_length=100)

    def __str__(self):
        return f"{self.item} ({self.quantity})"

class RecipeTag(models.Model):
    name = models.CharField(max_length=32, verbose_name='태그명')

    def __str__(self):
        return f"{self.pk}. {self.name}"


class Recipe(models.Model):

    EQUIPMENT = [
        ('microwave', '전자레인지'),
        ('oven', '오븐'),
        ('air_fryer', '에어프라이어'),
    ]
    author = models.ForeignKey(to=User,related_name='recipes',on_delete=models.CASCADE, verbose_name='작성자', null = True, blank=True)
     #related_name 추가 역방향 참조 => user.recipes
    title =  models.CharField('레시피명', max_length=100)
    represent_image = models.ImageField('대표이미지')
    tag = models.ManyToManyField(RecipeTag, blank=True)
    cookingTime = models.CharField('조리시간', max_length= 50)
    equipment = models.CharField(max_length=50, choices = EQUIPMENT)
    ingredients = models.ManyToManyField(Ingredient)


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE) 
    #related name 추가 역방향 참조 =>recipe.steps
    order = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField('이미지', blank=True, null=True)
    description = models.TextField('내용')

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.order is None:
            last_step = Step.objects.filter(recipe=self.recipe).order_by('-order').first()
            if last_step:
                self.order = last_step.order + 1
            else:
                self.order = 1

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order}: {self.description[:50]}"

