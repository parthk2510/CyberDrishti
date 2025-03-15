from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/incidents', views.IncidentReportViewSet)

urlpatterns = [
    # ... existing URLs
    path('', views.incident_report_view, name='incident_report'),
    path('success/', views.incident_report_success, name='incident_report_success'),
    path('incident-report/', include('incident_report.urls')),
    path('', include(router.urls)),
]


# Add this to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
