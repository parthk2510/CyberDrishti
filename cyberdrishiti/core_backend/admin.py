from django.contrib import admin
from .models import PhishingDomain, DetectionLog, ContentAnalysis, DomainBehaviorAnalysis, SSLAnalysis, UICloneAnalysis

@admin.register(PhishingDomain)
class PhishingDomainAdmin(admin.ModelAdmin):
    list_display = ('url', 'domain_name', 'registration_date', 'is_phishing', 'overall_score')
    search_fields = ('url', 'domain_name')
    list_filter = ('is_phishing', 'registration_date')

@admin.register(DetectionLog)
class DetectionLogAdmin(admin.ModelAdmin):
    list_display = ('domain', 'detection_time', 'ai_confidence', 'action_taken')
    list_filter = ('detection_time', 'action_taken')
    search_fields = ('domain__url',)

@admin.register(ContentAnalysis)
class ContentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('domain', 'ssl_valid', 'domain_age', 'suspicious_elements', 'score')
    list_filter = ('ssl_valid',)

@admin.register(DomainBehaviorAnalysis)
class DomainBehaviorAnalysisAdmin(admin.ModelAdmin):
    list_display = ('domain', 'mx_exists', 'spf_exists', 'dmarc_exists', 'score')
    list_filter = ('mx_exists', 'spf_exists', 'dmarc_exists')

@admin.register(SSLAnalysis)
class SSLAnalysisAdmin(admin.ModelAdmin):
    list_display = ('domain', 'certificate_valid', 'hostname_match', 'tls_valid', 'score')
    list_filter = ('certificate_valid', 'hostname_match', 'tls_valid')

@admin.register(UICloneAnalysis)
class UICloneAnalysisAdmin(admin.ModelAdmin):
    list_display = ('domain', 'similar_to', 'similarity_score')
    list_filter = ('similar_to',)
    search_fields = ('domain__url', 'similar_to')
