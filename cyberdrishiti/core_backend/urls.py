from django.urls import path
from .views import DomainDetectionAPI
from .views import DomainDetectionAPI, DomainDetailAPI

urlpatterns = [
    path('domains/detect/', DomainDetectionAPI.as_view(), name='domain-detect-api'),
    path('domains/<int:pk>/', DomainDetailAPI.as_view(),
         name='domain-detail-api'),  # URL for retrieving domain by ID

]
