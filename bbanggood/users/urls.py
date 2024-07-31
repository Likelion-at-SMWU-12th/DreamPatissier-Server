from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from .views import *


urlpatterns = [
    path('saved-recipes/', SavedRecipeListView.as_view(), name='saved-recipe'),
    path('saved-recipes/<int:pk>',SavedRecipeDetailView.as_view(),name='saved-recipe-detail'),
    path('my-recipes/',MyRecipeListView.as_view(), name='my-recipe'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)