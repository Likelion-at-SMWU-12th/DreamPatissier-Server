from rest_framework import generics, status
from django.db.models import Q
from .models import Recipe, Bookmark
from .serializers import RecipeSerializer, RecipeListSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # GET에서 RecipeListSerializer 사용
        if self.request.method == 'GET':
            return RecipeListSerializer
        # POST에서 RecipeSerializer 사용
        return RecipeSerializer


    def perform_create(self, serializer):
    # 현재 로그인된 사용자를 레시피 author로 자동설정
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        # `request`를 serializer의 context에 추가하여 `get_is_owner` 메서드에서 사용 가능하도록 함
        return {'request': self.request}


class RecipeRetrieveUpdatelView(generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # `request`를 serializer의 context에 추가
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

    
'''@api_view(['GET'])
def search_recipe(request):
    # 쿼리 매개변수에서 'keywords'를 가져옴
    keywords = request.GET.get('keywords', '')
    
    if not keywords:
        return Response({"error": "No keywords provided"}, status=400)
    
    keyword_list = keywords.split()

    filter_conditions = Q()
    for keyword in keyword_list:
        keyword_conditions = Q()
        
        keyword_conditions |= Q(tags__icontains=keyword)
        keyword_conditions |= Q(equipment__icontains=keyword)
        
        # 모든 키워드에 대해 OR 조건으로 검색하기
        filter_conditions |= keyword_conditions

    # 조건을 만족하는 레시피를 필터링
    recipes = Recipe.objects.filter(filter_conditions).distinct()
    serializer = RecipeListSerializer(recipes, many=True)
    return Response(serializer.data)'''

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
    serializer = RecipeListSerializer(recipes, many=True)
    return Response(serializer.data)