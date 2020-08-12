"""iptv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.permissions import AllowAny
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include(("authentication.urls", "auth"),
                                 namespace="auth")),
    path('api/v2/auth/', include(("authentication.v2urls", "authv2"),
                                 namespace="authv2")),
    path('api/v1/livetv/', include(("liveTv.urls", "liveTv"),
                                 namespace="liveTv")),
    path('api/v1/archives/', include(("archives.urls", "archives"),
                                 namespace="archives")),
    path('api/v1/vods/', include(("vod.urls", "vod"),
                                     namespace="vod")),
    path('api/v1/packages/', include(("package.urls", "package"),
                                 namespace="package")),
    path('api/v1/radio/', include(("radio.urls", "radio"),
                                 namespace="radio")),
    path('api/v1/settings/', include(("settings.urls", "settings"),
                                 namespace="settings")),
    path('api/v1/pvr/', include(("pvr.urls", "pvr"), 
                                 namespace="pvr"))
]

if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
