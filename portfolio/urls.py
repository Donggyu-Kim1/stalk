from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('list/', views.PortfolioListView.as_view(), name='portfolio_list'),    # 만든 포트폴리오 리스트
    path('create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),   # 포트폴리오 만들기
    path('<int:pk>/', views.PortfolioReadView.as_view(), name='portfolio_read'),    # 저장된 포트폴리오의 원 그래프, 수익률 그래프를 보여줌
    path('delete/<int:pk>/', views.PortfolioDeleteView.as_view(), name='portfolio_delete'), # 포트폴리오 삭제
]