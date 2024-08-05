from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Bread
from users.models import Review
from .serializers import BreadSerializer, ReviewSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from cart.models import Cart, CartItem
from django.utils import timezone
from django.db.models import Q

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
def search_bread(request, keyword):
    # 검색어에서 # 제거 및 포함 여부 확인
    if keyword.startswith('#'):
        search_term = keyword
        plain_keyword = keyword.lstrip('#')
    else:
        search_term = f"#{keyword}"
        plain_keyword = keyword

    query = Q(name__icontains=plain_keyword) | Q(tags__icontains=search_term)
    breads = Bread.objects.filter(query).distinct()

    serializer = BreadSerializer(breads, many=True, context={'request': request})
    return Response(serializer.data)

class BreadDetailView(generics.RetrieveAPIView):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        product_data = BreadSerializer(product, context={'request': request}).data

        # 리뷰 데이터를 가져와서 추가
        reviews = Review.objects.filter(order_item__product=product)
        reviews_data = ReviewSerializer(reviews, many=True, context={'request': request}).data
        product_data['reviews'] = reviews_data

        return Response(product_data)

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