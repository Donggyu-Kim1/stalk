from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('stocks/', include('stocks.urls')),
    path('accounts/', include('accounts.urls')),
    path('forum/', include('forum.urls')),
]