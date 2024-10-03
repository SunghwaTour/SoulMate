# models.py
from django.db import models
import uuid

# User
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID를 기본키로 사용
    username = models.CharField(max_length=255, unique=True)  # 사용자 이름 (중복 불가)
    password = models.CharField(max_length=255, unique=True)  # 비밀번호 (중복 불가)
    nickname = models.CharField(max_length=255, unique=True)  # 닉네임 (중복 불가)
    phone_number = models.CharField(max_length=15, unique=True)  # 전화번호 (중복 불가)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # 프로필 사진
    introduction = models.CharField(max_length=500, null=True, blank=True)  # 자기소개
    phone_number_verified = models.BooleanField(default=False) # 전화번호 인증 여부