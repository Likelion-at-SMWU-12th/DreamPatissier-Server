from rest_framework import serializers
from .models import User, Review, Order, OrderItem
from bakery.models import Bread

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = "__all__"
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = BreadSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order_item = OrderItemSerializer(read_only=True)
    order_item_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderItem.objects.all(),
        write_only=True,  # 쓰기 전용
        source='order_item'  # 실제 필드명
    )
    satisfaction = serializers.ChoiceField(choices=Review.SATISFACTION_CHOICES)

    class Meta:
        model = Review
        fields = ['id', 'user', 'order_item', 'order_item_id', 'content', 'satisfaction', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        return super().create(validated_data)