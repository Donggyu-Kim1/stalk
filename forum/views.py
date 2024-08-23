from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from .models import Forum, Post, Comment

class ForumListView(ListView):
    model = Forum
    template_name = 'forum/forum_list.html'
    context_object_name = 'forums'

class PostsListView(ListView):
    model = Post
    template_name = 'forum/posts_list.html'
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('forum_posts_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_liked'] = self.object.likes.filter(id=self.request.user.id).exists()
        return context

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['title', 'content']
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('forum_post_detail', kwargs={'post_id': self.object.id})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'
    success_url = reverse_lazy('forum_posts_list')
    pk_url_kwarg = 'post_id'

class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

class CommentsListView(ListView):
    model = Comment
    template_name = 'forum/comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return Comment.objects.filter(post=self.post)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'forum/comment_form.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum_post_detail', kwargs={'post_id': self.kwargs['post_id']})

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'forum/comment_detail.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'forum/comment_form.html'
    fields = ['content']
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('forum_post_detail', kwargs={'post_id': self.object.post.id})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'forum/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('forum_post_detail', kwargs={'post_id': self.object.post.id})
