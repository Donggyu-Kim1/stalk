from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('list/', views.PortfolioListView.as_view(), name='portfolio_list'),
    path('create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('read/', views.PortfolioReadView.as_view(), name='portfolio_read'),
    path('update/', views.PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('delete/', views.PortfolioDeleteView.as_view(), name='portfolio_delete'),
    path('detail/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
    ]