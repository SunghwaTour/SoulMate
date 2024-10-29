from django.contrib import admin
from .models import Board, Comment, Like

# Register your models here.
admin.site.register(Board)
admin.site.register(Comment)
admin.site.register(Like)
