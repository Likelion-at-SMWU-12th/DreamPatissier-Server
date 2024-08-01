from django.db import models
from django.contrib.auth.models import AbstractUser
from bakery.models import Bread

class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Bread, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Review(models.Model):
    SATISFACTION_CHOICES = [
        ('D', '별로예요'),
        ('S', '만족해요'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Bread, on_delete=models.CASCADE) 
    content = models.TextField()
    satisfaction = models.CharField(max_length=1, choices=SATISFACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'