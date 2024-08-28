from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)  # 게시물 제목
    content = models.TextField()  # 게시물 내용
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # 작성자
    created_at = models.DateTimeField(default=timezone.now)  # 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간
    views = models.PositiveIntegerField(default=0)  # 조회수
    stock_ticker = models.ForeignKey('stocks.Stock', on_delete=models.CASCADE, db_column='stock_id')  # 주식 티커

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 연결된 게시물
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # 작성자
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(default=timezone.now)  # 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


