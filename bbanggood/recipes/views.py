from rest_framework import generics
from .models import Recipe
from .serializers import RecipeSerializer, RecipeListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class RecipeListCreateAPIView(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
    # `list` 액션일 때는 RecipeListSerializer를 사용하고, 나머지에서는 RecipeSerializer를 사용
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer


    def perform_create(self, serializer):
    # 현재 로그인된 사용자를 레시피 author로 자동설정
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        # `request`를 serializer의 context에 추가하여 `get_is_owner` 메서드에서 사용 가능하도록 함
        return {'request': self.request}