from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('saved-recipes/', SavedRecipeListView.as_view(), name='saved-recipe'),
    path('saved-recipes/<int:pk>', SavedRecipeDetailView.as_view(), name='saved-recipe-detail'),
    path('my-recipes/', MyRecipeListView.as_view(), name='my-recipe'),
    path('my-recipes/<int:pk>', MyRecipeDetailView.as_view(), name='my-recipe-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
