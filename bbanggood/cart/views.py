from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from users.models import Order, OrderItem
from users.serializers import OrderSerializer
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'detail': 'No cart found.'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        try:
            with transaction.atomic():
                # 주문 생성
                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price
                )
                
                # 주문 항목 생성
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                
                # 장바구니 비우기
                cart_items.delete()
                
                # 주문 생성 결과 반환
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
