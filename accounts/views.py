from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm


class SignUpView(CreateView):
    '''
    장고 기본 회원가입 기능
    '''
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class CustomLoginView(LoginView):
    '''
    장고 기본 로그인 기능, 성공 시 base.html로 이동
    '''
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    '''
    로그아웃 시 로그인 페이지로 이동
    '''
    next_page = 'login'


class ProfileView(LoginRequiredMixin, DetailView):
    '''
    프로필 기능, User 테이블 사용
    '''
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    '''
    프로필 수정 기능, UserProfileForm 사용
    '''
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

