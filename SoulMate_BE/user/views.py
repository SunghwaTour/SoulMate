from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, SignUpSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .twilio import generate_verification_code, send_verification_code
from django.core.cache import cache  # Django 캐시 사용


# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny]) 
def register(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        # 전화번호 인증이 완료된 사용자만 회원가입 완료
        user = serializer.save()
        response = {
            'result':'true',
            'user_id' : user.user_id,
            'message':'회원가입이 완료되었습니다.'
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    data = 1 if 'non_field_errors' in serializer.errors else 2
    sta = status.HTTP_200_OK if 'non_field_errors' in serializer.errors else status.HTTP_400_BAD_REQUEST
    response = { 
        'result' : 'false',
        'data' : data,
        'message': serializer.errors,
    }
    return Response(response, status=sta)

# 로그인
@api_view(['POST'])
@permission_classes([AllowAny])  # 누구나 접근 가능
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        
        # 사용자 인증
        user = serializer.validated_data['user']
        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                'refresh': refresh_token,
                'access': access_token,
                'user_id': user.user_id,
                'username': user.username,
                'nickname': user.nickname
            }
            return Response({
                'result': 'true',
                'data': response_data,
                'message': '로그인 성공'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'result': 'false',
                'message': '잘못된 사용자명 또는 비밀번호입니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'result': 'false',
        'message': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# 토큰 재발급
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    serializer = TokenRefreshSerializer(data=request.data)

    try:
        # 토큰 유효성 검사
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        # 토큰이 유효하지 않거나 만료된 경우
        return Response({
            'result': 'false',
            'data': None,
            'message': {'token': ['토큰이 유효하지 않거나 만료 됐습니다']}
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 유효한 경우, 새로운 access 토큰 반환
    response_data = serializer.validated_data
    return Response({
        'result': 'true',
        'data': response_data,
        'message': '토큰 재발급 성공'
    }, status=status.HTTP_200_OK)

# 프로필 조회 뷰
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    profile_picture_url = user.profile_picture.url if user.profile_picture else None
    response_data = {
        'user_id': user.user_id,
        'username': user.username,
        'nickname': user.nickname,
        'profile_picture' : profile_picture_url
    }
    return Response({
        'result': 'true',
        'data': response_data,
        'message': '프로필 정보'
    }, status=status.HTTP_200_OK)


# 아이디 찾기
@api_view(['POST'])
@permission_classes([AllowAny])
def find_username(request) :
    # 전화번호를 받아온다
    phone_number = request.data.get('phone_number')

    # 전화번호를 입력하지 않았을 경우
    if not phone_number :
        response = {
            'result' : False,
            'message' : '전화번호를 입력해주세요'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    
    try:
        # 전화번호를 통해 원하는 객체 찾기
        user = User.objects.get(phone_number=phone_number)

        response = {
            'result' : True,
            'message' : '아이디가 성공적으로 반환되었습니다',
            'username' : user.username
        }
        return Response(response, status=status.HTTP_200_OK)
    
    # 객체가 없을 경우
    except User.DoesNotExist :
        response = {
            'result' : False,
            'message' : '해당 전화번호로 등록된 사용자가 없습니다'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    

# 비밀번호 찾기
@api_view(['POST'])
@permission_classes([AllowAny])
def find_password(request) :
    # 아이디와 전화번호 받아오기
    username = request.data.get('username')
    phone_number = request.data.get('phone_number')

    # 아이디와 전화번호를 입력하지 않았을 경우
    if not username and phone_number :
        response = {
            'result' : False,
            'message' : '아이디와 전화번호를 입력해주세요'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    try :
        # 아이디와 전화번호를 통해 원하는 객체 찾기
        user = User.objects.get(username=username, phone_number=phone_number)

        response = {
            'result' : True,
            'message' : '비밀번호가 성공적으로 반환되었습니다',
            'password' : user.password
        }
        return Response(response, status=status.HTTP_200_OK)
    
    # 객체가 없을 경우
    except User.DoesNotExist :
        response = {
            'result' : False,
            'message' : '해당 아이디와 전화번호로 등록된 사용자는 없습니다'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

# 전화번호 인증 코드 전송
@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request) :
    phone_number = request.data.get('phone_number')

    if not phone_number :
        response = {
            'result' : False,
            'message' : '전화번호를 입력해주세요'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 인증 코드 생성 및 전송
        verification_code = generate_verification_code()
        send_verification_code(phone_number, verification_code)

        # 인증 코드를 캐시에 저장 (5분 동안 유지)
        cache.set(phone_number, verification_code, timeout=300) 
        

        response = {
            'result': True,
            'message': '인증 코드가 성공적으로 전송되었습니다.'
        }
        return Response(response, status=status.HTTP_200_OK)
    
    except Exception as e:
        response = {
            'result': False,
            'message': str(e)           
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
# 전화번호 인증 코드 검증 
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    phone_number = request.data.get('phone_number')
    verification_code = request.data.get('verification_code')

    if not phone_number or not verification_code:
        
        return Response({
            'result': False,
            'message': '전화번호와 인증 코드를 모두 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 캐시에서 저장된 인증 코드 가져오기
    stored_code = cache.get(phone_number)

    if stored_code is None:
        
        return Response({
            'result': 'false',
            'message': '인증 코드가 만료되었거나 잘못된 전화번호입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if verification_code == stored_code:
        
        # 인증 성공 처리
        return Response({
            'result': True,
            'message': '인증이 성공적으로 완료되었습니다.'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'result': False,
            'message': '잘못된 인증 코드입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)