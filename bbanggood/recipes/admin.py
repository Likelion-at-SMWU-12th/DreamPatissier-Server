# admin.py
from django.contrib import admin
from .models import Recipe, Ingredient, Step, Bookmark

# Ingredient 모델을 관리
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')  
    search_fields = ('item',)  

# Step 모델을 관리
class StepAdmin(admin.ModelAdmin):
    list_display = ('description', 'image')  
    search_fields = ('description',)  

# Recipe 모델을 관리
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cookingTime')  # 리스트에서 보여줄 필드
    search_fields = ('title', 'author', 'tags')  # 검색 가능한 필드
    filter_horizontal = ('ingredients', 'steps')  # ManyToManyField를 위한 필터

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Bookmark)