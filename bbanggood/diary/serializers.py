from rest_framework import serializers
from .models import BreadDiary

class BreadDiarySerializer(serializers.ModelSerializer):
    img_src = serializers.SerializerMethodField()
    
    class Meta:
        model = BreadDiary
        fields = '__all__'
        
    def get_img_src(self, obj):
        request = self.context.get('request')
        if obj.img_src and hasattr(obj.img_src, 'url'):
            return request.build_absolute_uri(obj.img_src.url)
        return None