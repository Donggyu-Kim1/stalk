from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.accountSignupView.as_view(), name='accounts_signup'),  # 회원가입
    path('login/', views.accountLoginView.as_view(), name='accounts_login'),  # 로그인
    path('profile/', views.accountProfileView.as_view(), name='accounts_profile'),  # 프로필 설정
]
