from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.StocksSearchView.as_view(), name='stocks_search'),  # 주식 검색 창
    path('<str:ticker>/', views.StocksIntroView.as_view(), name='stocks_intro'),  # 주식 소개 글
    path('<str:ticker>/news/', views.StocksNewsView.as_view(), name='stocks_news'),  # 기업 관련 뉴스
    path('<str:ticker>/chart/', views.StocksChartView.as_view(), name='stocks_chart'),  # 주가 차트
    path('<str:ticker>/financials/', views.StocksFinancialsView.as_view(), name='stocks_financials'),  # 기업 재무 정보
]
