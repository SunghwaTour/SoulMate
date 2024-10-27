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
    user  = models.ForeignKey(User, on_delete=models.CASCADE, null=False) # 작성자

class Comment(models.Model) :
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False) # 게시판
    user  = models.ForeignKey(User, on_delete=models.CASCADE, null=False) # 작성자
    content = models.TextField(null=False) # 댓글 내용
    created_At = models.DateTimeField(auto_now_add=True) # 작성일
    updated_At = models.DateTimeField(auto_now=True) # 수정일