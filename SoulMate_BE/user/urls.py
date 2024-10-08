from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),  # 회원가입 엔드포인트
    path('token/refresh', views.refresh_token, name='token_refresh'),
    path('login/', views.login, name='login'),  # 로그인
    path('my_profile/', views.my_profile, name='my_profile'),  # 프로필 조회 엔드포인트
    path('username/', views.find_username, name="find_username"), # 아이디 찾기
    path('password/', views.find_password, name='find_password') # 비밀번호 찾기
]