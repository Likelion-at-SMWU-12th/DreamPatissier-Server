from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Review, Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import UserSerializer, ReviewSerializer, OrderSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
from rest_framework.response import Response
from rest_framework import status

class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'detail': 'No cart found.'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


