from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # 추가적인 회원가입 후처리가 필요하다면 여기서 처리
        return response

class LoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

class LogoutView(LogoutView):
    next_page = reverse_lazy('accounts_login')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('accounts_profile')

    def get_object(self):
        return self.request.user

class VerifyView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/verify.html'

    def post(self, request, *args, **kwargs):
        # 주주 인증 처리 로직 구현
        return self.render_to_response(self.get_context_data())