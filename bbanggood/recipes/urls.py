from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from .views import *


urlpatterns = [
    path('recipes/search/', search_recipe, name='recipe-search'),
    path('recipes/', RecipeListCreateView.as_view()),
    path('recipes/<int:pk>/',RecipeRetrieveUpdatelView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)