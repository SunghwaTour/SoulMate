from django.db import models
from user.models import User
import uuid

# Create your models here.
class Board(models.Model) :
    board_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=True) # 키값
    title = models.CharField(max_length=50, null=False) # 제목
    content = models.TextField(null=False) # 내용
    created_At = models.DateTimeField(auto_now_add=True) # 작성일
    updated_At = models.DateTimeField(auto_now=True) # 수정일
    user  = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자
    like_count = models.PositiveIntegerField(default=0) # 좋아요 개수 추가

class Comment(models.Model) :
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE) # 게시판
    user  = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자
    content = models.TextField(null=False) # 댓글 내용
    created_At = models.DateTimeField(auto_now_add=True) # 작성일
    updated_At = models.DateTimeField(auto_now=True) # 수정일
    like_count = models.PositiveIntegerField(default=0) # 좋아요 개수 추가

class Like(models.Model) :
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_At = models.DateTimeField(auto_now_add=True) # 작성일

    class Meta:
        unique_together = ('user', 'board', 'comment')  # 중복 좋아요 방지
