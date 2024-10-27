from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Board, Comment
from .serializers import BoardSerializer, BoardListSerializer, CommentSerializer

# 게시물 전체 조회
class BoardList(ListAPIView):
    queryset = Board.objects.all().order_by('-created_At')  # 전체 게시물 조회, 생성순 정렬
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        # 전체 게시물 조회
        boards = self.get_queryset()
        serializer = self.get_serializer(boards, many=True)

        return Response({
            'result': True,
            'message': '게시물 전체 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class BoardDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # 개별 게시글 가져오기
    def get_object(self, board_id):
        try:
            return Board.objects.get(board_id=board_id)  # UUID 필드 확인
        except Board.DoesNotExist:
            return Response({
                'result': False,
                'message': '게시물을 찾을 수 없습니다.',
                'data': 0
            }, status=status.HTTP_404_NOT_FOUND)

    # 게시글 상세 조회
    def get(self, request, board_id) :
        # 객체를 가져오기
        board = self.get_object(board_id)

        # 만약 get_object가 Response를 반환하면 그대로 return
        if isinstance(board, Response):
            return board
        
        serializer = BoardSerializer(board)

        return Response({
            'result': True,
            'message': '게시물 세부 조회 성공',
            'data': serializer.data
        })

    # 게시물 생성
    def post(self, request) :
        serializer = BoardSerializer(data=request.data)

        if serializer.is_valid() :
            board = serializer.save(user=request.user) # 작성자를 현재 로그인한 사용자로 설정
            return Response({
                'result' : True,
                'message' : "게시물 작성 성공",
                'data' : {
                    'board_id' : board.board_id
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'result' : False,
            'message' : '게시물 생성 실패',
            'data' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    # 게시글 수정
    def put(self, request, board_id):
        # 객체를 가져오기
        board = self.get_object(board_id)

        # 만약 get_object가 Response를 반환하면 그대로 return
        if isinstance(board, Response):
            return board

        # 작성자가 본인인지 확인
        print(board.user)
        print(request.user)
        if board.user != request.user:
            return Response({
                'result': False,
                'message': '본인만 게시물 수정이 가능합니다.',
                'data': 0
            }, status=status.HTTP_403_FORBIDDEN)

        # 수정 작업 수행
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'result': True,
                'message': '게시물 수정을 성공했습니다.',
                'data': {
                    'board_id': board.board_id
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'result': False,
            'message': '게시물 수정에 실패했습니다.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 게시물 삭제
    def delete(self, request, board_id) :
        # 객체를 가져오기
        board = self.get_object(board_id)

        # 만약 get_object가 Response를 반환하면 그대로 return
        if isinstance(board, Response):
            return board
        
        # 작성자가 본인인지 확인
        if board.user != request.user:
            return Response({
                'result': False,
                'message': '본인만 게시물 수정이 가능합니다.',
                'data': 0
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 게시물 삭제
        board.delete()

        return Response({
            'result': True,
            'message': '게시물을 삭제하였습니다.',
            'data': 1
        }, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 사용자만 작성 가능

    # 개별 게시글 가져오기
    def get_object(self, board_id):
        try:
            return Board.objects.get(board_id=board_id)  # UUID 필드 확인
        except Board.DoesNotExist:
            return Response({
                'result': False,
                'message': '게시물을 찾을 수 없습니다.',
                'data': 0
            }, status=status.HTTP_404_NOT_FOUND)
        
    # 댓글 조회
    def get(self, request, board_id) :
        
        board = self.get_object(board_id)
        comments = Comment.objects.filter(board=board).order_by('created_At')
        serializer = CommentSerializer(comments, many=True)
        
        return Response({
            'result': True,
            'message': '댓글 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


    # 댓글 작성
    def post(self, request, board_id) :

        board = self.get_object(board_id)

         # 만약 get_object가 Response를 반환하면 그대로 return
        if isinstance(board, Response):
            return board
        
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid() :
            comment = serializer.save(board=board, user=request.user)

            return Response({
                'result' : True,
                'message' : '댓글 작성 성공',
                'data' : {
                    'comment_id' : comment.comment_id
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'result' : False,
            'message' : '댓글 작성 실패',
            'data' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
