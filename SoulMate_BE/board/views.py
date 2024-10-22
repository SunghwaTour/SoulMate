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
    # POST : /board/
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
        
    # 게시물 수정
    # UPDATE : /board/{board_id}/
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 작성자가 본인인지 확인
        if instance.user != request.user :
            return Response({
                'result' : False,
                'message' : '본인만 게시물 작성이 가능합니다',
                'data' : 0
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 작성자가 맞으면, 수정 가능
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid() :
            serializer.save()

            return Response({
                'result' : True,
                'message' : '게시물이 수정되었습니다',
                'data' : serializer.data
            }, status=status.HTTP_200_OK)
        
        else :
            return Response({
                'result' : False,
                'message' : '게시물 수정에 실패했습니다.',
                'data' : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    # 게시글 삭제
    # DELETE : /board/{board_id}
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        # 작성자가 본인인지 확인
        if instance.user != request.user :
            return Response({
                'result' : False,
                'message' : '본인만 게시물 작성이 가능합니다',
                'data' : 0
            }, status=status.HTTP_403_FORBIDDEN)


        return Response({
            'result' : True,
            'message' : '게시물을 삭제하였습니다',
            'data' : 1
        },status=status.HTTP_204_NO_CONTENT)





