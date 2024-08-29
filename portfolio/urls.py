from django.urls import path
from . import views


app_name = 'portfolio'


urlpatterns = [
    path('list/', views.PortfolioListView.as_view(), name='portfolio_list'),
    path('create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('<int:pk>/', views.PortfolioReadView.as_view(), name='portfolio_read'),
    path('update/<int:pk>/', views.PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('delete/<int:pk>/', views.PortfolioDeleteView.as_view(), name='portfolio_delete'),
]