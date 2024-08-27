from django.urls import path
from . import views

urlpatterns = [
    path('', views.ForumMainView.as_view(), name='forum_main'),  # 주주 토론방 메인
    path('list/', views.ForumListView.as_view(), name='forum_list'),  # 글 리스트
    path('create/', views.PostCreateView.as_view(), name='post_create'),  # 글 작성
    path('<int:post_id>/', views.PostReadView.as_view(), name='post_read'),  # 글 읽기
    path('<int:post_id>/detail/', views.PostDetailView.as_view(), name='post_detail'),  # 글 추천, 조회수
    path('<int:post_id>/update/', views.PostUpdateView.as_view(), name='post_update'),  # 글 수정
    path('<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # 글 삭제
    path('<int:post_id>/comments/', views.PostCommentListView.as_view(), name='post_comment_list'),  # 댓글 리스트
    path('<int:post_id>/comments/create/', views.PostCommentCreateView.as_view(), name='post_comment_create'),  # 댓글/대댓글 작성
    path('<int:post_id>/comments/<int:comment_id>/', views.PostCommentDetailView.as_view(), name='post_comment_detail'),  # 댓글 수정/삭제
]
