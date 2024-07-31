from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from .views import *


urlpatterns = [
    path('search/', search_recipe, name='recipe-search'),
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/',RecipeRetrieveUpdateDestroyView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)