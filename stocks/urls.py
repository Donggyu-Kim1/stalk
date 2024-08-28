from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('search/', views.StocksSearchView.as_view(), name='search'),  # 주식 검색 창
    path('intro/<str:ticker>/', views.StocksIntroView.as_view(), name='intro'),  # 주식 소개 글
    path('news/<str:ticker>/', views.StocksNewsView.as_view(), name='news'),  # 기업 관련 뉴스
    path('chart/<str:ticker>/', views.StocksChartView.as_view(), name='chart'),  # 주가 차트
    path('financials/<str:ticker>/', views.StocksFinancialsView.as_view(), name='financials'),  # 기업 재무 정보
]
