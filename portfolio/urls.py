from django.urls import path
from .views import PortfolioListView, PortfolioCreateView, PortfolioDetailView, PortfolioStocksView

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio_list'),  # /portfolio/
    path('create/', PortfolioCreateView.as_view(), name='portfolio_create'),  # /portfolio/create/
    path('<int:portfolio_id>/', PortfolioDetailView.as_view(), name='portfolio_detail'),  # /portfolio/<int:portfolio_id>/
    path('<int:portfolio_id>/stocks/', PortfolioStocksView.as_view(), name='portfolio_stocks'),  # /portfolio/<int:portfolio_id>/stocks/
]
