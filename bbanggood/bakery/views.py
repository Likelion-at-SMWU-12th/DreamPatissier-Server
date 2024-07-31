from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Bread
from .serializers import BreadSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from cart.models import Cart, CartItem
from django.utils import timezone

class BreadViewSet(viewsets.ModelViewSet):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class BreadByCategoryView(generics.ListAPIView):
    serializer_class = BreadSerializer

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')

        if category_name not in dict(Bread.CATEGORY_CHOICES).keys():
            raise NotFound("Category not found.")
        
        return Bread.objects.filter(category=category_name)
    
    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
def search_bread(request, keywords):
    breads = Bread.objects.filter(title__icontains=keywords)
    serializer = BreadSerializer(breads, many=True)
    return Response(serializer.data)

class BreadDetailView(generics.RetrieveAPIView):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class AddToCartView(generics.GenericAPIView):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

    def post(self, request, *args, **kwargs):
        bread = self.get_object()  # pk로 Bread 객체를 가져오기

        user = request.user

        # 현재 사용자의 장바구니를 가져오거나 새로 만들기
        cart, created = Cart.objects.get_or_create(user=user, defaults={'created_at': timezone.now()})

        # 장바구니에 Bread 아이템 추가
        cart_item, created = CartItem.objects.get_or_create(cart=cart, bread=bread)
        if not created:
            # 이미 장바구니에 있는 아이템인 경우 수량을 업데이트합니다
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
            cart_item.save()
        
        return Response({'status': '장바구니에 추가되었습니다.'}, status=status.HTTP_200_OK)
