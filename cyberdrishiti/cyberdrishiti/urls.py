"""cyberdrishiti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
"""cyberdrishiti URL Configuration"""

from django.urls import path, include
from django.contrib import admin
from core_backend.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core_backend.urls')),
    path('', homepage, name='homepage'),
    # Include URLs from your app
]
