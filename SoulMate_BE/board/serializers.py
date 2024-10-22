from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Board
        fields = ['board_id', 'title', 'content', 'created_At', 'updated_At', 'user']