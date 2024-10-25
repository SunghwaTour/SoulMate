from rest_framework import serializers
from .models import Board

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