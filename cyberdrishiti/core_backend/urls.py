from django.urls import path
from .views import DomainDetectionAPI

urlpatterns = [
    path('domains/detect/', DomainDetectionAPI.as_view(), name='domain-detect-api'),
]
