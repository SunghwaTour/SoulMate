from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')

        # 직접 normalize_username 메서드를 정의하지 않는 경우 제거
        # 또는 추가로 정규화 작업이 필요하다면 여기에 추가
        # 예를 들어: username = username.lower() 
        # 만약 소문자로 정규화하려는 경우

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

# User
class User(AbstractBaseUser, PermissionsMixin):
    is_anonymous = False
    is_authenticated = True
    is_active = True

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID를 기본키로 사용
    username = models.CharField(max_length=255, unique=True)  # 사용자 이름 (중복 불가)
    password = models.CharField(max_length=255, unique=True)  # 비밀번호 (중복 불가)
    nickname = models.CharField(max_length=255, unique=True)  # 닉네임 (중복 불가)
    phone_number = models.CharField(max_length=15, unique=True)  # 전화번호 (중복 불가)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default_image.jpg')
    introduction = models.CharField(max_length=500, null=True, blank=True)  # 자기소개
    phone_number_verified = models.BooleanField(default=False) # 전화번호 인증 여부  
    
    is_active = models.BooleanField(default=True)  # 사용자 활성화 여부
    is_staff = models.BooleanField(default=False)  # 관리자 여부
    
    is_superuser = models.BooleanField(default=False)  # 관리자 여부 추가
    last_login = models.DateTimeField(null=True, blank=True)  # 마지막 로그인 시간 필드 추가


    USERNAME_FIELD = 'username'  # 로그인에 사용할 필드 지정
    REQUIRED_FIELDS = ['nickname', 'phone_number']  # 추가로 필요한 필드가 있다면 이 리스트에 추가

    objects = UserManager()

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        # 비밀번호를 해시하여 저장
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        # 해시된 비밀번호와 사용자가 입력한 비밀번호를 비교 
        return check_password(raw_password, self.password)