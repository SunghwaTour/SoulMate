from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


from .models import Board
from .serializers import BoardSerializer

# viewsets을 이용한
# 게시판 생성, 수정, 삭제, 조회
class BoardViewSet(viewsets.ModelViewSet) :
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    # 게시물 생성
    # POST : /boards/
    def create(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() :
            serializer.save(user=self.request.user) # 작성자를 로그인된 사용자로 설정
            
            response = {
                'result': True,
                'message': '게시물이 성공적으로 생성되었습니다.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                'result': False,
                'message': '게시물 생성에 실패했습니다.',
                'data': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



