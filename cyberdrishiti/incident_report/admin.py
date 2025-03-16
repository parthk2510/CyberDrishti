from django.contrib import admin
from .models import IncidentReport, IncidentAction, IncidentArtifact

class IncidentActionInline(admin.TabularInline):
    model = IncidentAction
    extra = 0

class IncidentArtifactInline(admin.TabularInline):
    model = IncidentArtifact
    extra = 0

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'incident_type', 'severity', 'status', 'reported_at', 'affected_domain')
    list_filter = ('status', 'severity', 'incident_type', 'auto_generated')
    search_fields = ('title', 'description', 'affected_domain__url')
    readonly_fields = ('reported_at',)
    inlines = [IncidentActionInline, IncidentArtifactInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'incident_type', 'severity', 'status')
        }),
        ('Reporting Information', {
            'fields': ('reported_by', 'reported_at', 'resolved_at', 'auto_generated')
        }),
        ('Related Data', {
            'fields': ('affected_domain',)
        }),
    )

@admin.register(IncidentAction)
class IncidentActionAdmin(admin.ModelAdmin):
    list_display = ('incident', 'action_time', 'action_by')
    list_filter = ('action_time',)
    search_fields = ('incident__title', 'action_taken', 'action_by')

@admin.register(IncidentArtifact)
class IncidentArtifactAdmin(admin.ModelAdmin):
    list_display = ('name', 'incident', 'artifact_type', 'uploaded_at')
    list_filter = ('artifact_type', 'uploaded_at')
    search_fields = ('name', 'incident__title', 'notes') 