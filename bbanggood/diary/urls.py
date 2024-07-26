from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreadDiaryViewSet

router = DefaultRouter()
router.register(r'diary', BreadDiaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# GET /diary/: 모든 일기 목록 조회
# POST /diary/: 새로운 일기 추가
# GET /diary/by_date/?date=YYYY-MM-DD: 특정 날짜에 해당하는 일기 목록 조회
# GET /diary/{id}/detail/: 특정 일기 상세 조회
# PUT /diary/{id}/: 특정 일기 수정
# DELETE /diary/{id}/: 특정 일기 삭제