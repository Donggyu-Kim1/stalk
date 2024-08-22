from django.urls import path
from .views import ForumListView, PostsListView, PostCreateView, PostDetailView, CommentsListView, CommentCreateView, CommentDetailView

urlpatterns = [
    path('', ForumListView.as_view(), name='forum_list'),  # /forum/
    path('posts/', PostsListView.as_view(), name='forum_posts_list'),  # /forum/posts/
    path('posts/create/', PostCreateView.as_view(), name='forum_post_create'),  # /forum/posts/create/
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='forum_post_detail'),  # /forum/posts/<int:post_id>/
    path('posts/<int:post_id>/comments/', CommentsListView.as_view(), name='forum_comments'),  # /forum/posts/<int:post_id>/comments/
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='forum_comment_create'),  # /forum/posts/<int:post_id>/comments/create/
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='forum_comment_detail'),  # /forum/posts/<int:post_id>/comments/<int:comment_id>/
]
