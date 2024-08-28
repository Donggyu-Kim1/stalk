from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Comment
from stocks.models import Stock
from .forms import PostForm, CommentForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('created_at')
        context['form'] = CommentForm()  # 댓글 작성 폼 추가
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect('forum:post_read', ticker=self.kwargs['ticker'], post_id=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

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


class PostCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'forum/post_comment_update.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={
            'ticker': self.object.post.stock_ticker.ticker,
            'post_id': self.object.post.post_id
        })


class PostCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'forum/post_comment_delete.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('forum:post_read', kwargs={
            'ticker': self.object.post.stock_ticker.ticker,
            'post_id': self.object.post.post_id
        })