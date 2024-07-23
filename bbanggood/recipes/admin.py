from django.contrib import admin
from .models import *
# Register your models here.

class StepInline(admin.TabularInline):
    model= Step
    extra = 1
# admin.py
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')
    search_fields = ('item',)

@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cookingTime', 'equipment')
    inlines = [StepInline]
    search_fields = ('title', 'author__username', 'ingredients__item', 'tag__name')
    filter_horizontal = ('tag', 'ingredients')

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'order', 'description')
    search_fields = ('recipe__title', 'description')
    list_filter = ('recipe',)
