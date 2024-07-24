from django.conf.urls.static import static
from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from .views import *

router= routers.DefaultRouter()
router.register(r'recipes',RecipeListCreateAPIView)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)