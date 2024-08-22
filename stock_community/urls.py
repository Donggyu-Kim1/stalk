from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stocks/', include('stocks.urls')),  # stocks 앱 URL
    path('accounts/', include('accounts.urls')),  # accounts 앱 URL
    path('forum/', include('forum.urls')),  # forum 앱 URL
    path('portfolio/', include('portfolio.urls')),  # portfolio 앱 URL
]
