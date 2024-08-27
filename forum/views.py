from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from stocks.models import Stock
from .models import Post, Comment


class ForumMainView(View):
    def get(self, request, ticker=None):
        context = {}
        if ticker:
            company = get_object_or_404(Stock, ticker=ticker)
            context['company'] = company
            context['recent_posts'] = Post.objects.filter(stock=company).order_by('-created_at')[:5]
        return render(request, 'forum_main.html', context)


class ForumListView(ListView):
    model = Post
    template_name = 'forum_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'stock']
    template_name = 'post_create.html'
    success_url = reverse_lazy('forum_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostReadView(DetailView):
    model = Post
    template_name = 'post_read.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save()
        return response


class PostDetailView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if 'like' in request.POST:
            post.likes += 1
            post.save()
        return redirect('post_read', post_id=post_id)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'stock']
    template_name = 'post_update.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('post_read', kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('forum_list')
    pk_url_kwarg = 'post_id'


class PostCommentListView(ListView):
    model = Comment
    template_name = 'post_comment_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])


class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'post_comment_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_read', kwargs={'post_id': self.kwargs['post_id']})


class PostCommentDetailView(LoginRequiredMixin, View):
    def get(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        return render(request, 'post_comment_detail.html', {'comment': comment})

    def post(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if 'update' in request.POST:
            comment.content = request.POST['content']
            comment.save()
        elif 'delete' in request.POST:
            comment.delete()
        return redirect('post_read', post_id=post_id)