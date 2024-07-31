from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from bakery.models import Bread  # 'bakery' 앱에서 Bread 모델을 가져옴

class Cart(models.Model): #장바구니 정보(장바구니 자체)
    user = get_user_model()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model): #장바구니에 담긴 아이템 정보 -> Bread와 동일
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.bread.name} in {self.cart.user.username}'s Cart"
