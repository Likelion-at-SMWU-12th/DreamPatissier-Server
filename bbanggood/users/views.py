from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipes.models import Recipe, Bookmark
from recipes.serializers import RecipeListSerializer, RecipeSerializer

# Create your views here.

#내가 작성한 레시피



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