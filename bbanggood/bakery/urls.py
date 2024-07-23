# bakery/urls.py
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreadViewSet, BreadByCategoryView, search_bread, BreadDetailView, AddToCartView

router = DefaultRouter()
router.register(r'bakery', BreadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bakery/category/<str:category_name>/', BreadByCategoryView.as_view(), name='bread-by-category'),
    path('bakery/search/<str:keywords>/', search_bread, name='bread-search'),
    path('bakery/<int:pk>/', BreadDetailView.as_view(), name='bread-detail'),
    path('bakery/<int:pk>/add/', AddToCartView.as_view(), name='add-to-cart'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)