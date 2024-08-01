from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReviewViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls))
]
