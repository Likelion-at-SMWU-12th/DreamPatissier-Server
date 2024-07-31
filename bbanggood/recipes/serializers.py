from rest_framework import serializers
from .models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    # 새로운 필드 추가
    is_owner = serializers.SerializerMethodField()
    author = serializers.CharField()  # 사용자 이름을 문자열로 입력받기

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'image', 'author', 'tags', 'cookingTime', 'equipment',
            'ingredients', 'step1_image', 'step1_description', 'step2_image', 'step2_description',
            'step3_image', 'step3_description', 'step4_image', 'step4_description',
            'step5_image', 'step5_description', 'step6_image', 'step6_description',
            'step7_image', 'step7_description', 'step8_image', 'step8_description',
            'step9_image', 'step9_description', 'step10_image', 'step10_description',
            'is_owner'
        ]

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False

    def create(self, validated_data):
        # username으로 author를 찾는 과정
        author_username = self.context['request'].data.get('author')
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'author': 'Invalid username'})
        
        # author를 validated_data에 추가하고 Recipe 인스턴스 생성
        validated_data['author'] = author
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # username으로 author를 찾는 과정
        author_username = self.context['request'].data.get('author')
        if author_username:
            try:
                author = User.objects.get(username=author_username)
                validated_data['author'] = author
            except User.DoesNotExist:
                raise serializers.ValidationError({'author': 'Invalid username'})
        
        return super().update(instance, validated_data)
    
from rest_framework import serializers
from .models import Recipe

class RecipeListSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'image', 'title', 'equipment', 'tags', 'is_owner']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False
    
    
