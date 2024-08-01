from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipes.models import Recipe, Bookmark
from recipes.serializers import RecipeListSerializer, RecipeSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Review, Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import UserSerializer, ReviewSerializer, OrderSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

#내가 작성한 레시피

class MyRecipeListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = RecipeListSerializer

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(author=user)
    
class MyRecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer

    def get_object(self):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        
        return Recipe.objects.get(author=user, id=recipe_id)
    
#저장한 레시피

class SavedRecipeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeListSerializer

    def get_queryset(self):
        user = self.request.user
        # 사용자가 북마크한 레시피를 필터링
        return Recipe.objects.filter(bookmarks__user=user).distinct()
    
class SavedRecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_object(self):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        return Recipe.objects.filter(bookmarks__user=user, id=recipe_id).first()
    
    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('pk')
        user = request.user
        recipe = Recipe.objects.get(id=recipe_id)
        
        # 북마크 추가/제거 처리
        bookmark, created = Bookmark.objects.get_or_create(user=user, recipe=recipe)
        
        if created:
            return Response({'message': 'Recipe bookmarked'}, status=status.HTTP_201_CREATED)
        else:
            bookmark.delete()
            return Response({'message': 'Recipe unbookmarked'}, status=status.HTTP_204_NO_CONTENT)
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
from rest_framework.response import Response
from rest_framework import status

# 주문 처리 뷰
class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

# 리뷰 처리 뷰
class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)

