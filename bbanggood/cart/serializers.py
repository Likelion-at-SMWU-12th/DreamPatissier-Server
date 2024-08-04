from rest_framework import serializers
from bakery.models import Bread  # 'bakery' 앱에서 Bread 모델을 가져옴
from .models import Cart, CartItem

class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    bread = BreadSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'bread', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']