"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from rest_framework import routers

from apps.auth import views as auth_views

from apps.blogs.views import PostViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/csrf/', auth_views.csrf),
    path('auth/login/', auth_views.login),
    path('auth/status/', auth_views.status),

    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router.urls)),
]
