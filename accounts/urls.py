from django.urls import path
from .views import SignupView, LoginView, LogoutView, ProfileView, VerifyView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='accounts_signup'),  # /accounts/signup/
    path('login/', LoginView.as_view(), name='accounts_login'),  # /accounts/login/
    path('logout/', LogoutView.as_view(), name='accounts_logout'),  # /accounts/logout/
    path('profile/', ProfileView.as_view(), name='accounts_profile'),  # /accounts/profile/
    path('verify/', VerifyView.as_view(), name='accounts_verify'),  # /accounts/verify/
]
