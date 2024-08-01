from rest_framework import serializers
from .models import ResultType
from bakery.models import Bread

#왜 이런 오류가 나는거지?
class ResultTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResultType
        fields = ['title', 'image', 'description1', 'description2', 'description3']

class RecommendBreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = ['id','name', 'img_src', 'tags']
