from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import *

# Create your views here.

User = get_user_model()

class QuestionView(APIView):
    def get(self, request, page_number):
        #페이지별로 질문지 구성하기
        questions = {
        1: {"question": "빵을 구경하던 당신, 어떤 빵소개가 더 마음에 드나요?", "choices": ["다이어트할 때 걱정 없이 행복하게 먹을 수 있는 베이글","비건빵이라 우유와 버터가 들어 있지 않고 밀가루도 넣지 않아 속이 편한 베이글"]},
            2:{"question": "먹어본 적이 없는 인기빵을 구매할 때, 당신이 선택한 이유는 무엇인가요?", "choices": ["(리뷰를 본 후) 리뷰가 좋으니까 구매해야지!","오늘은 새로운 걸 시도해보고 싶으니까~"]},
            3:{"question": "레시피대로 빵을 만들던 중, 레시피와 모양이 다른 빵을 만들어졌을 때의 반응은 무엇인가요?", "choices": ["레시피랑 달라도 새로운 빵이 만들어지다니 완전 럭키비키잖아~","오늘은 새로운 걸 시도해보고 싶으니까~"]},
            4:{"question": "친구한테 온 연락! 우울해서 빵을 샀다고 했을 때 당신의 반응은 무엇인가요?", "choices": ["무슨 빵을 샀을까? 크림빵?","왜 우울한지 궁금하다"]},
            5:{"question": "빵을 사러 나갔을 때, 당신의 선택 방법은 무엇인가요?", "choices": ["빵집의 메뉴를 미리 살펴보고 어떤 빵을 사고 싶은지 결정해 두었다.","빵집에 가서 그때 그때 눈에 들어오는 빵을 고른다."]},
            6:{"question": "친구가 새로운 빵을 추천할 때, 당신의 반응은 무엇인가요?", "choices": ["친구가 그 빵을 좋아하는 이유와 맛이 궁금하다.","빵의 성분, 영양정보, 다른 사람들의 리뷰가 궁금하다."]}
        }

        question_data = questions.get(page_number, {"question":"질문은 6번이 마지막입니다","choices":[]})

        return Response(question_data, status = status.HTTP_200_OK)
    
class SubmitView(APIView):
    def post(self, request):
        #요청을 보낸 사용자(로그인된 사용자) 정보 연결
        user = request.user
        data = request.data
        result = data.get('result')

        #유형 결과에 따른 id 설정
        if result == 'FP':
            result_id =  1
        elif result == 'FJ':
            result_id = 2
        elif result == 'TP':
            result_id = 3
        elif result == 'TJ':
            result_id = 4
        else:
            return Response({"알림: 존재하지 않는 유형결과입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        #기존 유형 테스트 결과가 있다면 필터링하여 업데이트
        existing_result = Result.objects.filter(user=user).first()
        
        if existing_result:
            existing_result.result_id = result_id
            existing_result.save()  

        else:
            Result.objects.create(user=user, result_id=result_id)      
        
        return Response({"message": "답변이 저장되었습니다", "result_id": result_id}, status=status.HTTP_201_CREATED)
    
