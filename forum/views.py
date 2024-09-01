from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from stocks.models import Stock
from .forms import PostForm, CommentForm


class ForumMainView(ListView):
    '''
    Post 모델, 템필릿에서 리스트 표시 시 posts 사용
    url에서 ticker 값을 가져와 해당 티커의 값을 가진 post만 가져옴
    최신순 정렬
    제목 or 내용에 있는 글자를 쿼리로 검색할 수 있게 함
    티커 값이 Stock 테이블에 없는 값이면 404 에러
    '''
    model = Post
    template_name = 'forum/forum_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(stock_ticker__ticker=self.kwargs['ticker']).order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock'] = get_object_or_404(Stock, ticker=self.kwargs['ticker'])
        context['query'] = self.request.GET.get('q', '')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    '''
    PostForm 사용
    로그인한 유저만 PostCreateView에 접근할 수 있도록 LoginRequiredMixin 사용
    성공 시 동일 티커 값을 가진 리스트 페이지로 이동
    '''
    model = Post
    form_class = PostForm
    template_name = 'forum/post_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.stock_ticker = get_object_or_404(Stock, ticker=self.kwargs['ticker'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:forum_list', kwargs={'ticker': self.kwargs['ticker']})


class PostReadView(DetailView):
    '''
    pk_url_kwarg 값 post_id 지정
    get_object 할때마다 views 1씩 증가
    댓글 기능, 부모가 없는 경우 댓글, 부모가 있는 경우 대댓글
    모델에 담길 수 있도록 유효성 검사
    '''
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
        context['comments'] = Comment.objects.filter(post=self.object, parent=None).order_by('created_at')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            comment.save()
            return redirect('forum:post_read', ticker=self.kwargs['ticker'], post_id=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    수정기능, Post Form
    로그인한 유저만 PostUpdateView에 접근할 수 있도록 LoginRequiredMixin, UserPassesTestMixin 사용
    성공 시 동일 ticker 값을 가진 리드 페이지로 이동
    '''
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
    '''
    삭제 기능, 동일 티커 list로 이동
    '''
    model = Post
    template_name = 'forum/post_delete.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('forum:forum_list', kwargs={'ticker': self.kwargs['ticker']})


class PostCommentListView(ListView):
    '''
    댓글 리스트, 템플릿에서 read 뷰에 include
    '''
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
    '''
    댓글 수정 기능, 각 모델의 참조 값에 따라 read 뷰로 이동
    '''
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
    '''
    댓글 삭제 기능
    '''
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