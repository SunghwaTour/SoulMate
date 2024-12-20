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
from django.contrib.auth.hashers import make_password
from django.utils import timezone



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
    
    # 전화번호 인증이 완료되었는지 확인
    if not cache.get(f"verified_{phone_number}"):
        return Response({
            'result': 'false',
            'message': '전화번호 인증이 완료되지 않았습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
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
    

# 비밀번호 재설정 요청
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_request(request) :
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
    
    # 전화번호 인증이 완료되었는지 확인
    if not cache.get(f"verified_{phone_number}"):
        return Response({
            'result': 'false',
            'message': '전화번호 인증이 완료되지 않았습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)


    try :
        # 아이디와 전화번호를 통해 원하는 객체 찾기
        user = User.objects.get(username=username, phone_number=phone_number)

        response = {
            'result' : True,
            'message' : '사용자가 확인되었습니다. 새로운 비밀번호를 입력해주세요.',
            'user_id' : user.user_id
        }
        return Response(response, status=status.HTTP_200_OK)
    
    # 객체가 없을 경우
    except User.DoesNotExist :
        response = {
            'result' : False,
            'message' : '해당 아이디와 전화번호로 등록된 사용자는 없습니다'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    
# 비밀번호 재설정
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    # 비밀번호 재설정을 위한 정보 받기
    user_id = request.data.get('user_id')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    # 비밀번호 입력 확인
    if not user_id or not password or not password_confirm:
        return Response({
            'result': False,
            'message': '비밀번호를 모두 입력해주세요'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 비밀번호 일치 확인
    if password != password_confirm:
        return Response({
            'result': False,
            'message': '비밀번호가 일치하지 않습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 사용자 찾기
        user = User.objects.get(user_id=user_id)
        
        # 비밀번호 재설정
        user.password = make_password(password)
        user.save()

        return Response({
            'result': True,
            'message': '비밀번호가 성공적으로 재설정되었습니다.'
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({
            'result': False,
            'message': '사용자를 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)

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

    # 요청 카운트 및 타임스탬프 가져오기
    request_count = cache.get(f'request_count_{phone_number}', 0)
    first_request_time = cache.get(f'first_request_time_{phone_number}')

    current_time = timezone.now()
    
    # 요청이 1시간(3600초) 이내일 경우 요청 카운트 증가
    if first_request_time:
        time_diff = (current_time - first_request_time).total_seconds()
        if time_diff < 360:  # 10분 이내
            if request_count >= 5:  # 최대 요청 횟수 제한 (예: 5회)
                response = {
                    'result': False,
                    'message': '인증 코드는 1시간마다 최대 5회 요청할 수 있습니다.'
                }
                return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)
            else:
                request_count += 1
        else:
            # 1시간 이상 지났으면 카운트 및 타임스탬프 리셋
            request_count = 1
            first_request_time = current_time
    else:
        # 처음 요청 시 타임스탬프 설정
        request_count = 1
        first_request_time = current_time

    # 현재 요청 시간 저장
    cache.set(f'first_request_time_{phone_number}', first_request_time, timeout=360)  # 타임스탬프 캐시에 저장 (10분 유지)
    cache.set(f'request_count_{phone_number}', request_count, timeout=360)  # 요청 카운트 캐시에 저장 (10분 유지)

    
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
        cache.set(f"verified_{phone_number}", True, timeout=3600)  # 인증 완료 상태 캐시에 저장
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