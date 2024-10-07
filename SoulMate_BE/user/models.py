# models.py
from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

# User
class User(models.Model):
    is_anonymous = False
    is_authenticated = True
    is_active = True

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID를 기본키로 사용
    username = models.CharField(max_length=255, unique=True)  # 사용자 이름 (중복 불가)
    password = models.CharField(max_length=255, unique=True)  # 비밀번호 (중복 불가)
    nickname = models.CharField(max_length=255, unique=True)  # 닉네임 (중복 불가)
    phone_number = models.CharField(max_length=15, unique=True)  # 전화번호 (중복 불가)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # 프로필 사진
    introduction = models.CharField(max_length=500, null=True, blank=True)  # 자기소개
    phone_number_verified = models.BooleanField(default=False) # 전화번호 인증 여부  

    USERNAME_FIELD = 'username'  # 로그인에 사용할 필드 지정
    REQUIRED_FIELDS = []  # 추가로 필요한 필드가 있다면 이 리스트에 추가

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        # 비밀번호를 해시하여 저장
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        # 해시된 비밀번호와 사용자가 입력한 비밀번호를 비교 
        return check_password(raw_password, self.password)