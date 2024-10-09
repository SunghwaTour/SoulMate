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

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny]) 
def register(request):

    # 전화번호가 인증되었는지 확인 (해당 유저의 is_verified 필드 확인)
    phone_number = request.data.get('phone_number')
    
    # try:
    #     user = User.objects.get(phone_number=phone_number)
    #     if not user.is_verified:
    #         return Response({"error": "전화번호 인증이 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
    # except User.DoesNotExist:
    #     return Response({"error": "해당 전화번호로 가입된 사용자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

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