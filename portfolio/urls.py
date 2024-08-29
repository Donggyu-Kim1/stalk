from django.urls import path
from . import views


app_name = 'portfolio'


urlpatterns = [
    path('list/', views.PortfolioListView.as_view(), name='portfolio_list'),    # 만든 포트폴리오 리스트
    path('search/', views.PortfolioSearchView.as_view(), name='portfolio_search'),  # 포트폴리오를 만들기 위한 주식 검색란
    path('create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),  # 검색 받은 주식의 티커를 불러오고 수량과 가격을 입력
    path('add_stock/', views.AddStockToPortfolioView.as_view(), name='add_stock_to_portfolio'), # 포트폴리오에 받을 주식 추가
    path('<int:pk>/', views.PortfolioReadView.as_view(), name='portfolio_read'),    # 저장된 포트폴리오의 원 그래프, 수익률 그래프를 보여줌
    path('update/<int:pk>/', views.PortfolioUpdateView.as_view(), name='portfolio_update'), #  포트폴리오 수정(수량과 가격)
    path('delete/<int:pk>/', views.PortfolioDeleteView.as_view(), name='portfolio_delete'), # 포트폴리오 삭제
]