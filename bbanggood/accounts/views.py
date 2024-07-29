from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse
# Create your views here.

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password2 = request.data.get('password2')
    last_name = request.data.get('last_name')
    
    #phone = request.data.get('phone', default = None)

    errors={}

    #username(아이디) 유효성 검사
    if not username:
        errors['username'] = '아이디는 필수 입력값입니다.'

    elif User.objects.filter(username=username).exists():
        errors['username'] = '이미 사용 중인 아이디입니다.'

    #비밀번호 형식 검사
    if password:
        try:
            validate_password(password)
        except ValidationError:
            errors['password'] = '올바른 형식으로 입력해주세요.'
    else:
        errors['password'] = '비밀번호는 필수 입력값입니다.'
    #비밀번호 중복검사
    if password and not password2:
        errors["password"] = '비밀번호를 한번 더 입력해주세요.'

    elif password and password != password2 :
        errors['password'] = '올바른 형식으로 입력해주세요.'
    
    #400 에러메시지 
    if errors:
        return Response({'errors': errors}, status= status.HTTP_400_BAD_REQUEST)

    
    user = User.objects.create_user(
        username=username,
        password = password,
        last_name = last_name,
        #phone = phone  //user 모델 커스텀 후 추가예정
    )

    #리디렉션 url
    signup_clear_url = reverse('accounts:signup-clear')

    return Response({'message':'회원가입 성공','data': request.data,'redirect_url':signup_clear_url},status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def signup_clear(request):
    #...
    return Response({'회원가입이 완료되었습니다!'},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    #사용자 입력정보 받아들이기
    username = request.data.get('username')
    password = request.data.get('password')

    errors = {}

    #이메일과 비밀번호 유효성 검사
    if not username:
        errors['username']= '아이디를 입력해 주세요.'
    if not password:
        errors['password'] = '비밀번호를 입력해 주세요.'

    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
       
    # 사용자 인증
    user = authenticate(request, username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'last_name': user.last_name})    
    
    else:
        errors['unauthorized']='아이디와 비밀번호를 정확히 입력해주세요.'
        return Response({'errors':errors},status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'message':'성공적으로 로그아웃 되었습니다.'}, status=status.HTTP_200_OK)