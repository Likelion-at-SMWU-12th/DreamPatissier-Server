# bakery/views.py

from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Bread
from .serializers import BreadSerializer

class BreadViewSet(viewsets.ModelViewSet):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

class BreadByCategoryView(generics.ListAPIView):
    serializer_class = BreadSerializer

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Bread.objects.filter(category=category_name)

from rest_framework.decorators import api_view

@api_view(['GET'])
def search_bread(request, keywords):
    breads = Bread.objects.filter(name__icontains=keywords)
    serializer = BreadSerializer(breads, many=True)
    return Response(serializer.data)

class BreadDetailView(generics.RetrieveAPIView):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

class AddToCartView(generics.UpdateAPIView):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # 장바구니에 추가하는 로직 구현
        return Response({'status': 'added to cart'})
