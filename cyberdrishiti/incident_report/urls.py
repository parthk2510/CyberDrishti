from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
schema_view = get_schema_view(title="CyberDrishti API")

urlpatterns = [
    # ... existing URLs
    path('Report_success/', views.incident_report_success,
         name='incident_report_success'),
    path('incident-report/', include('incident_report.urls')),
    # Web views
    path('dashboard/', views.incident_dashboard, name='incident_dashboard'),
    
    # API endpoints
    path('api/incidents/', views.IncidentReportListCreateView.as_view(), name='incident_list_create'),
    path('api/incidents/<uuid:pk>/', views.IncidentReportDetailView.as_view(), name='incident_detail'),
    path('api/incidents/<uuid:incident_id>/actions/', views.IncidentActionListCreateView.as_view(), name='incident_actions'),
    path('api/incidents/<uuid:incident_id>/artifacts/', views.IncidentArtifactListCreateView.as_view(), name='incident_artifacts'),
    path('api/auto-report/', views.AutoReportPhishingIncident.as_view(), name='auto_report_incident'),
]


# Add this to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
