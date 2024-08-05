from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import Recipe, Bookmark
from .serializers import RecipeSerializer, RecipeListSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 사용자만 생성 가능, 읽기는 인증 여부에 상관 없음

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        request = self.request
        author_username = request.data.get('author')
        if author_username:
            try:
                author = User.objects.get(username=author_username)
            except User.DoesNotExist:
                raise serializers.ValidationError({'author': 'Invalid username'})
            serializer.save(author=author)
        else:
            # 기본적으로 현재 로그인한 사용자를 author로 설정
            serializer.save(author=request.user)

class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user
        
        # 북마크 추가/제거 처리
        bookmark, created = Bookmark.objects.get_or_create(user=user, recipe=recipe)
        
        if created:
            return Response({'message': 'Recipe bookmarked'}, status=status.HTTP_201_CREATED)
        else:
            bookmark.delete()
            return Response({'message': 'Recipe unbookmarked'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def search_recipe(request):
    keywords = request.GET.get('keywords', '')
    
    if not keywords:
        return Response({"error": "No keywords provided"}, status=400)
    
    keyword_list = keywords.split()
    filter_conditions = Q()
    for keyword in keyword_list:
        keyword_conditions = Q(tags__icontains=keyword) | Q(equipment__icontains=keyword)
        filter_conditions &= keyword_conditions

    recipes = Recipe.objects.filter(filter_conditions).distinct()
    serializer = RecipeListSerializer(recipes, many=True, context={'request': request})
    return Response(serializer.data)
