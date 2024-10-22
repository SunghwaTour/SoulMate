from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet

# 라우터 생성
router = DefaultRouter()

# BoardViewSet에 대한 라우터 등록
router.register(r'', BoardViewSet)  # 'boards'는 URL 패턴에서 사용할 prefix

# URL 패턴 설정
urlpatterns = [
    path('', include(router.urls)),  # 등록된 라우터의 URL을 포함
]