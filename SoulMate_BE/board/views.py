from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Board, Comment, Like
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
                'message': '게시물을 찾을 수 없음',
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


class CommentDetailView(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 개별 댓글 가져오기
    def get_comment_object(self, board_id, comment_id):
        try:
            return Comment.objects.get(board_id=board_id, comment_id=comment_id)
        except Comment.DoesNotExist:
            return Response({
                'result' : False,
                'message' : '댓글을 찾을 수 없음',
                'data' : 0
            }, status=status.HTTP_404_NOT_FOUND)

    # 댓글 수정
    def put(self, request, board_id, comment_id) :
        # 원하는 댓글 객체 찾기
        comment = self.get_comment_object(board_id, comment_id)

         # 만약 get_comment_object가 Response를 반환하면 그대로 return
        if isinstance(comment, Response):
            return comment

        # 작성자 확인
        if comment.user != request.user :
            return Response({
                'result' : False,
                'message' : '본인만 댓글 수정 가능',
                'data' : 0
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid() :
            # 수정한 댓글 저장
            serializer.save()

            return Response({
                'result' : True,
                'message' : '댓글 수정 성공',
                'data' : {
                    'comment_id' : comment.comment_id
                }
            })
        
        return Response({
            'result' : False,
            'message' : '댓글 수정 실패',
            'data' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 삭제
    def delete(self, request, board_id, comment_id) :

        # 원하는 댓글 객체 찾기
        comment = self.get_comment_object(board_id, comment_id)

        # 만약 get_comment_object가 Response를 반환하면 그대로 return
        if isinstance(comment, Response):
            return comment

        if comment.user != request.user :
            return Response({
                'result' : False,
                'message' : '본인만 댓글 삭제 가능',
                'data' : 0
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 댓글 삭제
        comment.delete()

        return Response({
            'result' : True,
            'message' : '댓글 삭제 성공',
            'data' : 1
        })

class LikeView(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 게시물 객체 찾는 함수
    def get_object_board(self, target_id) :
        try :
            return Board.objects.get(board_id=target_id)
        except Board.DoesNotExist :
            return Response({
                'result' : False,
                'message' : '게시물을 찾을 수 없음',
                'data' : 0
            }, status=status.HTTP_404_NOT_FOUND)
        
    # 댓글 객체 찾는 함수
    def get_object_comment(self, target_id) :
        try :
            return Comment.objects.get(comment_id=target_id)
        except Comment.DoesNotExist :
            return Response({
                'result' : False,
                'message' : '댓글을 찾을 수 없음',
                'data' : 0
            }, status=status.HTTP_404_NOT_FOUND)

    # 좋아요 기능
    # 좋아요 없을 시 -> 추가
    # 좋아요 이미 있을 시 -> 삭제
    def post(self, request, target_type, target_id) :
        target = None

        # 좋아요 대상이 게시물일 경우
        if target_type == 'board' :
            target = self.get_object_board(target_id)

            if isinstance(target, Response) :
                return target

            like, created = Like.objects.get_or_create(user=request.user, board=target, comment=None)
        
        # 좋아요 대상이 댓글일 경우
        elif target_type == 'comment' :
            target = self.get_object_comment(target_id)

            if isinstance(target, Response) :
                return target
        
            like, created = Like.objects.get_or_create(user=request.user, board=None, comment=target)

        else :
            return Response({
                'result' : False,
                'message' : '잘못된 대상',
                'data' : 0
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 좋아요 추가 및 취소 처리
        if created:
            target.like_count += 1
            target.save()
            return Response({
                'result': True,
                'message': f'{target_type} 좋아요 추가',
                'data' : {
                    'like_count': target.like_count
                }
            }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            target.like_count -= 1
            target.save()
            return Response({
                'result': True,
                'message': f'{target_type} 좋아요 취소',
                'data' : {
                    'like_count': target.like_count
                }
            }, status=status.HTTP_200_OK)

