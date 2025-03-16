from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from . import views
from .views import ui_similarity_view

schema_view = get_schema_view(title="CyberDrishti API")

urlpatterns = [
    # Basic views
    path('', views.homepage, name='homepage'),
    path('analyze-ssl/', views.analyze_ssl_view, name='analyze_ssl'),

    # API endpoints
    path('domains/', views.DomainListCreateAPI.as_view(), name='domain_list'),
    path('domains/<uuid:pk>/', views.DomainDetailAPI.as_view(), name='domain_detail'),
    path('analyze/', views.PhishingAnalysisAPI.as_view(), name='phishing_analysis'),
    path('batch-analyze/', views.BatchAnalysisAPI.as_view(), name='batch_analysis'),

    # API Documentation
    path('docs/', include_docs_urls(title='CyberDrishti API')),
    path('schema/', schema_view, name='schema'),
    path('ui-similarity/', ui_similarity_view, name='ui-similarity'),
]
