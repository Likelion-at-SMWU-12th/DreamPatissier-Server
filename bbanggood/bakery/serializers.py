from rest_framework import serializers
from .models import Bread

class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'
