from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Post, Comment
from stocks.models import Stock
from .forms import PostForm, CommentForm  # 폼을 별도로 정의해야 합니다

class ForumMainView(ListView):
    model = Post
    template_name = 'forum/forum_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # 페이지당 10개의 게시글

    def get_queryset(self):
        self.stock = get_object_or_404(Stock, ticker=self.kwargs['ticker'])
        return Post.objects.filter(stock_ticker=self.stock).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock'] = self.stock
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.stock_ticker = get_object_or_404(Stock, ticker=self.kwargs['ticker'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:forum_list', kwargs={'ticker': self.kwargs['ticker']})

class PostReadView(DetailView):
    model = Post
    template_name = 'forum/post_read.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_update.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={'ticker': self.kwargs['ticker'], 'post_id': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_delete.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('forum:forum_list', kwargs={'ticker': self.kwargs['ticker']})

class PostCommentListView(ListView):
    model = Comment
    template_name = 'forum/post_comment_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=self.post).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context

class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/post_comment_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={'ticker': self.kwargs['ticker'], 'post_id': self.kwargs['post_id']})

class PostCommentDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/post_comment_detail.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={'ticker': self.kwargs['ticker'], 'post_id': self.object.post.pk})