from django.urls import path, include
from . import views

# URL 패턴 설정
urlpatterns = [
    path('', views.BoardDetail.as_view(), name='board-detail-create'), # 게시물 생성
    path('<uuid:board_id>/', views.BoardDetail.as_view(), name='board-detail'), # 게시물 수정, 삭제 
    path('all/', views.BoardList.as_view(), name='board-list'), # 게시물 전체 조회
    path('<uuid:board_id>/comment/', views.CommentListCreateView.as_view()), # 댓글 생성, 조회
    path('<uuid:board_id>/comment/<uuid:comment_id>/', views.CommentDetailView.as_view()) # 댓글 수정, 삭제
]