"""systems_monitoring URL Configuration
"""

from django.contrib import admin
from django.urls import path, re_path
from home.views import home
from django.urls.conf import include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='index'),
    path('api/v1/monitor/', include('monitor.urls')),

    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),

    # path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'.', home, name='index'),

 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
