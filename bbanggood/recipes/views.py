from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import Recipe, Bookmark
from .serializers import RecipeSerializer, RecipeListSerializer

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # 요청 메서드에 따라 적절한 serializer를 반환
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        # 사용자가 요청 시 제공한 username을 기반으로 author를 설정
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        # 요청 데이터에서 author를 username으로 처리
        author_username = request.data.get('author')
        if author_username:
            request.data._mutable = True
            request.data['author'] = author_username
            request.data._mutable = False
        
        return super().create(request, *args, **kwargs)

class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

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
    # 쿼리 매개변수에서 'keywords'를 가져오기
    keywords = request.GET.get('keywords', '')
    
    if not keywords:
        return Response({"error": "No keywords provided"}, status=400)
    
    keyword_list = keywords.split()

    # 모든 키워드에 대해 AND 조건으로 필터링
    filter_conditions = Q()
    for keyword in keyword_list:
        # 조건 생성
        keyword_conditions = Q(tags__icontains=keyword) | Q(equipment__icontains=keyword)
        
        # AND로 연결
        filter_conditions &= keyword_conditions

    # 조건을 만족하는 레시피를 필터링
    recipes = Recipe.objects.filter(filter_conditions).distinct()
    serializer = RecipeListSerializer(recipes, many=True, context={'request': request})
    return Response(serializer.data)