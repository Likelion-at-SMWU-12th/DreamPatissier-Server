from rest_framework import serializers
from .models import Bread
from users.serializers import ReviewSerializer

class BreadSerializer(serializers.ModelSerializer):
    img_src = serializers.SerializerMethodField()
    img_dtl = serializers.SerializerMethodField()  # img_dtl
    reviews = ReviewSerializer(many=True, read_only=True)  # 리뷰 직렬화기 추가
    
    class Meta:
        model = Bread
        fields = '__all__'  
        
    def get_img_src(self, obj):
        request = self.context.get('request')
        if obj.img_src and hasattr(obj.img_src, 'url'):
            return request.build_absolute_uri(obj.img_src.url)
        return None

    def get_img_dtl(self, obj):  # img_dtl
        request = self.context.get('request')
        if obj.img_dtl and hasattr(obj.img_dtl, 'url'):
            return request.build_absolute_uri(obj.img_dtl.url)
        return None