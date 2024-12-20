from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import *
from.serializers import ResultTypeSerializer, RecommendBreadSerializer
import random

# Create your views here.

User = get_user_model()

class QuestionView(APIView):
    def get(self, request, page_number):
        #페이지별로 질문지 구성하기
        questions = {
        1: {"question": "빵을 구경하던 당신,<br/>어떤 빵소개가 더 마음에 드나요?", "choices": [{"type":"F", "text":"다이어트할 때 걱정 없이 행복하게 먹을 수 있는 베이글"}, {"type" : "T", "text": "비건빵이라 우유와 버터가 들어 있지 않고 밀가루도 넣지 않아 속이 편한 베이글"}]},
        2:{"question": "먹어본 적이 없는<br/>인기빵을 구매할 때,<br/>당신이 선택한 이유는 무엇인가요?", "choices": [{"type":"J", "text":"(리뷰를 본 후) 리뷰가 좋으니까 구매해야지!"}, {"type" : "P", "text": "오늘은 새로운 걸 시도해보고 싶으니까~"}]},
        3:{"question": "레시피대로 빵을 만들던 중,<br/>레시피와 모양이 다른 빵이<br/>만들어졌을 때의 반응은 무엇인가요?", "choices": [{"type":"P", "text":"레시피랑 달라도 새로운 빵이 만들어지다니 완전 럭키비키잖아~"}, {"type" : "J", "text": "레시피대로 완성되지 않다니 너무 속상해.."}]},
            4:{"question": "친구한테 온 연락!<br/>우울해서 빵을 샀다고 했을 때<br/>당신의 반응은 무엇인가요?", "choices": [{"type":"T", "text":"무슨 빵을 샀을까? 크림빵?"}, {"type" : "F", "text": "왜 우울한지 궁금하다"}]},
            5:{"question": "빵을 사러 나갔을 때,<br/>당신의 선택 방법은 무엇인가요?", "choices": [{"type":"J", "text":"빵집의 메뉴를 미리 살펴보고 어떤 빵을 사고 싶은지 결정해 두었다."}, {"type" : "P", "text": "빵집에 가서 그때 그때 눈에 들어오는 빵을 고른다."}]},
            6:{"question": "친구가 새로운 빵을 추천할 때,<br/>당신의 반응은 무엇인가요?", "choices": [{"type":"F", "text":"친구가 그 빵을 좋아하는 이유와 맛이 궁금하다."}, {"type" : "T", "text": "빵의 성분, 영양정보, 다른 사람들의 리뷰가 궁금하다."}]}
        }

        question_data = questions.get(page_number, {"question":"질문은 6번이 마지막입니다","choices":[]})

        return Response(question_data, status = status.HTTP_200_OK)
    
class SubmitView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        #요청을 보낸 사용자(로그인된 사용자) 정보 연결
        user = request.user
        data = request.data
        result = data.get('result')

        #유형 결과에 따른 id 설정
        if result == 'FP':
            result_id =  1
            result_type = "폭신한 인기쟁이 식빵"
        elif result == 'FJ':
            result_id = 2
            result_type = "겉바속촉 바게트"
        elif result == 'TP':
            result_id = 3
            result_type = "달달한 해피바이러스 케이크"
        elif result == 'TJ':
            result_id = 4
            result_type = "속 든든한 완벽주의 베이글"
        else:
            return Response({"알림: 존재하지 않는 유형결과입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        #기존 유형 테스트 결과가 있다면 필터링하여 업데이트
        existing_result = Result.objects.filter(user=user).first()
        
        if existing_result:
            existing_result.result_id = result_id
            existing_result.result_type=result_type
            existing_result.save()  

        else:
            Result.objects.create(user=user, result_id=result_id,result_type=result_type) 

        result_url = f"/test/result/{result_id}"    
        
        return Response({"message": "답변이 저장되었습니다", "result_id": result_id,"result_type":result_type, "result_url":result_url}, status=status.HTTP_201_CREATED)


class ResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        
        if pk == 'null': #null일때 처리
            return redirect('/test/questions/1')

        try:
            pk = int(pk)
        except ValueError:
            return redirect('/test/questions/1') 


        result_type = get_object_or_404(ResultType, pk=pk)

        bread_recommendations = BreadRecommendation.objects.filter(result_type=result_type)
        recommend = random.sample(list(bread_recommendations), 2)

        bread_serializer = RecommendBreadSerializer([recommendation.bread for recommendation in recommend], many=True)
        breads = bread_serializer.data

        result_type_serializer = ResultTypeSerializer(result_type)
        result_type_data = result_type_serializer.data

       # Build absolute URIs for image fields
        result_type_data['image'] = request.build_absolute_uri(result_type_data['image'])
        for bread in breads:
            bread['img_src'] = request.build_absolute_uri(bread['img_src'])


        response_data = {
            "title": result_type_data['title'],
            "image": result_type_data['image'],
            "description1": result_type_data['description1'],
            "description2": result_type_data['description2'],
            "description3": result_type_data['description3'],
            "breads": breads
        }

        return Response(response_data, status=status.HTTP_200_OK)