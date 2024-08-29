from django.urls import path
from . import views


app_name = 'forum'


urlpatterns = [
    path('<str:ticker>/', views.ForumMainView.as_view(), name='forum_list'), # 특정 기업 토론방 메인
    path('<str:ticker>/create/', views.PostCreateView.as_view(), name='post_create'),  # 글 작성
    path('<str:ticker>/<int:post_id>/', views.PostReadView.as_view(), name='post_read'),  # 글 읽기, 댓글 작성
    path('<str:ticker>/<int:post_id>/update/', views.PostUpdateView.as_view(), name='post_update'),  # 글 수정
    path('<str:ticker>/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # 글 삭제
    path('<str:ticker>/<int:post_id>/comments/', views.PostCommentListView.as_view(), name='post_comment_list'),  # 댓글 리스트
    path('<str:ticker>/posts/<int:post_id>/comments/<int:comment_id>/update/', views.PostCommentUpdateView.as_view(), name='post_comment_update'),  # 댓글 수정
    path('<str:ticker>/posts/<int:post_id>/comments/<int:comment_id>/delete/', views.PostCommentDeleteView.as_view(), name='post_comment_delete'),  # 댓글 삭제
]
