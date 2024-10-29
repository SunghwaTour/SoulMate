from rest_framework import serializers
from .models import Board, Comment, Like

class BoardSerializer(serializers.ModelSerializer) :
    user = serializers.StringRelatedField()  # user 필드를 StringRelatedField로 설정

    class Meta :
        model = Board
        fields = ['board_id', 'title', 'content', 'created_At', 'updated_At', 'user']

class BoardListSerializer(serializers.ModelSerializer) :
    user = serializers.StringRelatedField()  # user 필드를 StringRelatedField로 설정

    class Meta : 
        model = Board
        fields = ['board_id', 'title', 'created_At', 'updated_At', 'user']

class CommentSerializer(serializers.ModelSerializer) :
    user = serializers.StringRelatedField()  # user 필드를 StringRelatedField로 설정
    board = serializers.PrimaryKeyRelatedField(read_only=True)  # board 필드도 읽기 전용

    class Meta :
        model = Comment
        fields = ['comment_id', 'board', 'user', 'content', 'created_At', 'updated_At']

class LikeSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Like
        fields = ['like_id', 'board', 'user', 'comment', 'created_At']
        read_only_fields = ['board', 'user', 'comment', 'created_At']
        