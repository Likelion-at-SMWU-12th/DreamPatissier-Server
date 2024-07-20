from django.shortcuts import render
from django.contrib.auth import login,logout, authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
# Create your views here.

User = get_user_model()

@api_view(['POST'])
def signup_api(request):
    data = request.data
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "회원가입이 완료되었습니다.","data": data})
    
    return Response(serializer.errors)
