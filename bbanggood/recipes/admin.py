# admin.py
from django.contrib import admin
from .models import Recipe, Ingredient, Step

# Ingredient 모델을 관리하기 위한 admin 클래스
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')  # 리스트에서 보여줄 필드
    search_fields = ('item',)  # 검색 가능한 필드

# Step 모델을 관리하기 위한 admin 클래스
class StepAdmin(admin.ModelAdmin):
    list_display = ('description', 'image')  # 리스트에서 보여줄 필드
    search_fields = ('description',)  # 검색 가능한 필드

# Recipe 모델을 관리하기 위한 admin 클래스
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cooking_time')  # 리스트에서 보여줄 필드
    search_fields = ('title', 'author', 'tags')  # 검색 가능한 필드
    filter_horizontal = ('ingredients', 'steps')  # ManyToManyField를 위한 필터

# 모델을 admin 사이트에 등록
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Recipe, RecipeAdmin)
