from rest_framework import serializers
from .models import Recipe, Ingredient, Step
from django.contrib.auth import get_user_model

User=get_user_model()

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['item', 'quantity']

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['image', 'description']

class RecipeSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)
    author = serializers.CharField()  # User 모델의 username을 직렬화

    class Meta:
        model = Recipe
        fields = ['id','author', 'image', 'title', 'tags', 'cookingTime', 'equipment', 'ingredients', 'steps','is_owner']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        steps_data = validated_data.pop('steps')
        author_username = validated_data.pop('author')
        
        # username으로 User 객체 가져오기
        try:
            user = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"author": "User with this username does not exist."})

        # Recipe 객체 생성
        recipe = Recipe.objects.create(author=user, **validated_data)

        
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            recipe.ingredients.add(ingredient)
        
        for step_data in steps_data:
            step, created = Step.objects.get_or_create(**step_data)
            recipe.steps.add(step)
        
        return recipe
    
    def update(self, instance, validated_data):
        # 기존의 연관 데이터 삭제
        instance.ingredients.clear()
        instance.steps.clear()

        # Recipe 데이터 업데이트
        instance.image = validated_data.get('image', instance.image)
        instance.title = validated_data.get('title', instance.title)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.cookingTime = validated_data.get('cookingTime', instance.cookingTime)
        instance.equipment = validated_data.get('equipment', instance.equipment)
        instance.save()

        # 새 연관 데이터 추가
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])

        for ingredient_data in ingredients_data:
            item = ingredient_data.get('item')
            quantity = ingredient_data.get('quantity')
            if item and quantity is not None:
                # item과 quantity 조합으로 유일성 판단
                ingredients = Ingredient.objects.filter(item=item, quantity=quantity)
                if ingredients.exists():
                    ingredient = ingredients.first()
                else:
                    ingredient = Ingredient.objects.create(item=item, quantity=quantity)
                instance.ingredients.add(ingredient)
            else:
                raise serializers.ValidationError({"ingredients": "재료이름 또는 수량이 생략되었습니다."})

        for step_data in steps_data:
            description = step_data.get('description')
            image = step_data.get('image')
            if description:
                #description을 기준으로 유일성 판단해서 수정
                steps = Step.objects.filter(description=description)
                if steps.exists():
                    step = steps.first()
                    step.image = image
                    step.save()
                else:
                    step = Step.objects.create(description=description, image=image)
                instance.steps.add(step)
            else:
                raise serializers.ValidationError({"steps": "설명이 생략되었습니다."})

        return instance

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