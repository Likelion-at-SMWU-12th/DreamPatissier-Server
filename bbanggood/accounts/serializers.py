from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=11, required= False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone']

    def validate(self, data):           

        if data.get('email'):
            try :
                validate_email(data['email'])
            except serializers.ValidationError:
                raise serializers.ValidationError({"email":"올바른 이메일 주소를 입력하세요. "})
            
        if data.get('password'):
            try: 
                validate_password(data['password'])
            
                if data['password'] != data['password2']:
                    raise serializers.ValidationError({"password":"비밀번호가 일치하지 않습니다."})
            except:
                raise serializers.ValidationError({"password":"올바른 형식으로 입력해주세요"})
            
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email'],
        )
        phone = validated_data.get('phone')
        if phone:
            pass

        return user