from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
# Create your views here.

User = get_user_model()

@api_view(['POST'])
def signup_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    password2 = request.data.get('password2')
    username = request.data.get('username')
    #phone = request.data.get('phone', default = None)

    errors={}
    #이메일 형식 검사
    if email:
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = '올바른 형식으로 입력해주세요'
    else:
        errors['email'] = '이메일은 필수 입력값입니다.'
    #비밀번호 형식 검사
    if password:
        try:
            validate_password(password)
        except ValidationError:
            errors['password'] = '올바른 형식으로 입력해주세요.'
    else:
        errors['password'] = '비밀번호는 필수 입력값입니다.'
    #비밀번호 중복검사
    if password != password2 :
        errors['password'] = '올바른 형식으로 입력해주세요.'

    if User.objects.filter(username=username).exists():
        errors['username'] = '이미 사용 중인 이름입니다.'
    #400 에러메시지 
    if errors:
        return Response({'errors': errors}, status= status.HTTP_400_BAD_REQUEST)

    
    user = User.objects.create_user(
        email = email,
        username=username,
        password = password,
        #phone = phone  //user 모델 커스텀 후 추가예정
    )

    #리디렉션 url
    signup_clear_url = reverse('accounts:signup-clear')

    return Response({'message':'회원가입 성공','data': request.data,'redirect_url':signup_clear_url},status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def signup_clear(request):
    #...
    return Response({'회원가입이 완료되었습니다!'},status=status.HTTP_200_OK)