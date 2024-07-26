from rest_framework import serializers
from .models import BreadDiary

class BreadDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BreadDiary
        fields = '__all__'
