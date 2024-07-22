from django.contrib import admin
from .models import *
# Register your models here.

class StepInline(admin.TabularInline):
    model= Step
    extra = 1
# admin.py
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name',)

@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cook_time', 'equipment')
    inlines = [StepInline]
    search_fields = ('title', 'author__username', 'ingredients__name', 'tag__name')
    filter_horizontal = ('tag', 'ingredients')

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'order', 'instruction')
    search_fields = ('recipe__title', 'instruction')
    list_filter = ('recipe',)
