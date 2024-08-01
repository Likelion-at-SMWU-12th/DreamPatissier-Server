from django.contrib import admin
from .models import User, Order, OrderItem, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)