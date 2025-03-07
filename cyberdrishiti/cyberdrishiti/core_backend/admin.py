from django.contrib import admin
from .models import PhishingDomain, DetectionLog


@admin.register(PhishingDomain)
class PhishingDomainAdmin(admin.ModelAdmin):
    list_display = ('url', 'registrar', 'status', 'threat_score')
    list_filter = ('status', 'registrar')
    search_fields = ('url',)


@admin.register(DetectionLog)
class DetectionLogAdmin(admin.ModelAdmin):
    list_display = ('domain', 'detection_time', 'ai_confidence')
    readonly_fields = ('detection_time',)
