from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Bread
from .serializers import BreadSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view

class BreadViewSet(viewsets.ModelViewSet):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

class BreadByCategoryView(generics.ListAPIView):
    serializer_class = BreadSerializer

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')

        if category_name not in dict(Bread.CATEGORY_CHOICES).keys():
            raise NotFound("Category not found.")
        
        return Bread.objects.filter(category=category_name)

@api_view(['GET'])
def search_bread(request, keywords):
    breads = Bread.objects.filter(title__icontains=keywords)
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
        # Implement logic to add to cart here
        return Response({'status': 'added to cart'})
