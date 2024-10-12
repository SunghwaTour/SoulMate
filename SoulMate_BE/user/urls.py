from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),  # 회원가입 엔드포인트
    path('token/refresh', views.refresh_token, name='token_refresh'),
    path('login/', views.login, name='login'),  # 로그인
    path('my_profile/', views.my_profile, name='my_profile'),  # 프로필 조회 엔드포인트
    path('username/', views.find_username, name="find_username"), # 아이디 찾기
    path('password/reset/', views.reset_password_request, name='reset_password_request'), # 비밀번호 재설정 요청
    path("password/", views.reset_password, name="reset_password"), # 비밀번호 재설정
    path('send/code/', views.send_code, name='send_code'), # 전화번호 인증 코드 전송
    path('verify/code/', views.verify_code, name='verify_code'), # 전화번호 인증 코드 확인
]