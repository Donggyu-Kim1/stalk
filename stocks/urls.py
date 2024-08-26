from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.stocksSearchView.as_view(), name='stocks_search'),  # 주식 검색 창
    path('<str:symbol>/', views.stocksIntroView.as_view(), name='stocks_intro'),  # 주식 소개 글
    path('<str:symbol>/news/', views.stocksNewsView.as_view(), name='stocks_news'),  # 기업 관련 뉴스
    path('<str:symbol>/chart/', views.stocksChartView.as_view(), name='stocks_chart'),  # 주가 차트
    path('<str:symbol>/financials/', views.stocksFinancialsView.as_view(), name='stocks_financials'),  # 기업 재무 정보
]
