from django.contrib import admin
from .models import IncidentReport

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_role', 'email', 'reporter_type', 'created_at')
    list_filter = ('reporter_type', 'reporter_identity', 'is_critical', 'created_at')
    search_fields = ('name_role', 'email', 'organization_name', 'affected_entity', 'incident_description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Reporter Information', {
            'fields': ('reporter_type', 'reporter_identity', 'name_role', 'organization_name', 
                      'contact_no', 'email', 'address')
        }),
        ('Basic Incident Details', {
            'fields': ('affected_entity', 'incident_types', 'other_incident_details', 
                      'is_critical', 'critical_details')
        }),
        ('System Information', {
            'fields': ('system_info', 'domain_url', 'ip_address', 'operating_system', 
                      'make_model', 'app_details', 'location', 'isp_info')
        }),
        ('Incident Description', {
            'fields': ('incident_description', 'occurrence_date', 'detection_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    ) 