from django.urls import path
from .views import (
    ForumListView, PostsListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView,
    PostLikeView, CommentsListView, CommentCreateView, CommentDetailView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path('', ForumListView.as_view(), name='forum_list'),
    path('posts/', PostsListView.as_view(), name='forum_posts_list'),
    path('posts/create/', PostCreateView.as_view(), name='forum_post_create'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='forum_post_detail'),
    path('posts/<int:post_id>/update/', PostUpdateView.as_view(), name='forum_post_update'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='forum_post_delete'),
    path('posts/<int:post_id>/like/', PostLikeView.as_view(), name='forum_post_like'),
    path('posts/<int:post_id>/comments/', CommentsListView.as_view(), name='forum_comments'),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='forum_comment_create'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='forum_comment_detail'),
    path('posts/<int:post_id>/comments/<int:comment_id>/update/', CommentUpdateView.as_view(), name='forum_comment_update'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='forum_comment_delete'),
]
