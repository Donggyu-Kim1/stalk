from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('search/', views.StocksSearchView.as_view(), name='search'),
    path('detail/<str:pk>/', views.StockDetailView.as_view(), name='detail'),
]
