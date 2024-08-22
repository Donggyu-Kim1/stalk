from django.urls import path
from .views import StocksListView, StocksCompanyView, StocksNewsView, StocksChartView, StocksFinancialsView

urlpatterns = [
    path('', StocksListView.as_view(), name='stocks_list'),  # /stocks/
    path('company/', StocksCompanyView.as_view(), name='stocks_company'),  # /stocks/company/
    path('news/', StocksNewsView.as_view(), name='stocks_news'),  # /stocks/news/
    path('chart/', StocksChartView.as_view(), name='stocks_chart'),  # /stocks/chart/
    path('financials/', StocksFinancialsView.as_view(), name='stocks_financials'),  # /stocks/financials/
]
