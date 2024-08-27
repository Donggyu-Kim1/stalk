from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm

class ForumMainView(ListView):
    model = Post
    template_name = 'forum/forum_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(stock_ticker=self.kwargs['ticker'])

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.stock_ticker = self.kwargs['ticker']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:forum_list', kwargs={'ticker': self.kwargs['ticker']})

class PostReadView(DetailView):
    model = Post
    template_name = 'forum/post_read.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'], stock_ticker=self.kwargs['ticker'])

class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_update.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={'ticker': self.kwargs['ticker'], 'post_id': self.object.id})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'forum/post_delete.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('forum:forum_list', kwargs={'ticker': self.kwargs['ticker']})

class PostCommentListView(ListView):
    model = Comment
    template_name = 'forum/post_comment_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/post_comment_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={'ticker': self.kwargs['ticker'], 'post_id': self.kwargs['post_id']})

class PostCommentDetailView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/post_comment_detail.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={'ticker': self.kwargs['ticker'], 'post_id': self.kwargs['post_id']})