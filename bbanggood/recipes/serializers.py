# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Recipe, Bookmark

User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()  # 문자열로 변환된 사용자 이름
    is_scrapped = serializers.SerializerMethodField() #is_scrapped 필드 추가

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'image', 'author', 'tags', 'cookingTime', 'equipment', 
            'ingredients', 'step1_image', 'step1_description',
            'step2_image', 'step2_description', 'step3_image', 'step3_description',
            'step4_image', 'step4_description', 'step5_image', 'step5_description',
            'step6_image', 'step6_description', 'step7_image', 'step7_description',
            'step8_image', 'step8_description', 'step9_image', 'step9_description',
            'step10_image', 'step10_description', 'is_owner','is_scrapped'
        ]
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False
    
    #is_scrapped 필드를 필터링으로 정의
    def get_is_scrapped(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, recipe=obj).exists()
        return False 

    def create(self, validated_data):
        request = self.context['request']
        author_username = request.data.get('author')
        if not author_username:
            raise serializers.ValidationError({'author': 'Username is required'})
        
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'author': 'Invalid username'})
        
        validated_data['author'] = author
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        author_username = request.data.get('author')
        if author_username:
            try:
                author = User.objects.get(username=author_username)
                validated_data['author'] = author
            except User.DoesNotExist:
                raise serializers.ValidationError({'author': 'Invalid username'})
        
        return super().update(instance, validated_data)

class RecipeListSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    is_scrapped = serializers.SerializerMethodField() #is_scrapped 필드 추가

    class Meta:
        model = Recipe
        fields = ['id', 'image', 'title', 'equipment', 'tags', 'cookingTime','is_owner','is_scrapped']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False
    
    #is_scrapped 필드를 필터링으로 정의
    def get_is_scrapped(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, recipe=obj).exists()
        return False
