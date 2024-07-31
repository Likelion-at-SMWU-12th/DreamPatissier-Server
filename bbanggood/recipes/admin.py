from django.contrib import admin
from .models import Recipe, Bookmark

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tags', 'cookingTime', 'equipment')
    search_fields = ('title', 'tags', 'cookingTime', 'equipment')
    list_filter = ('author', 'tags')

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('user', 'recipe')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Bookmark, BookmarkAdmin)