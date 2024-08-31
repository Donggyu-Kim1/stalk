from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.StockIndexView.as_view(), name='home'),
    path('stocks/', include('stocks.urls')),
    path('accounts/', include('accounts.urls')),
    path('forum/', include('forum.urls')),
    path('portfolio/', include('portfolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)