# File: cyberdrishiti/core_backend/serializers.py
from rest_framework import serializers
from .models import PhishingDomain, ContentAnalysis, DomainBehaviorAnalysis, SSLAnalysis, UICloneAnalysis, DetectionLog


class PhishingDomainSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PhishingDomain
        fields = '__all__'

class ContentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentAnalysis
        exclude = ('domain',)

class DomainBehaviorAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainBehaviorAnalysis
        exclude = ('domain',)

class SSLAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSLAnalysis
        exclude = ('domain',)

class UICloneAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UICloneAnalysis
        exclude = ('domain',)

class DetectionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionLog
        exclude = ('domain',)

class AnalysisResultSerializer(serializers.ModelSerializer):
    content_analysis = ContentAnalysisSerializer(read_only=True)
    behavior_analysis = DomainBehaviorAnalysisSerializer(read_only=True)
    ssl_analysis = SSLAnalysisSerializer(read_only=True)
    ui_analysis = UICloneAnalysisSerializer(read_only=True)
    recent_logs = serializers.SerializerMethodField()
    
    class Meta:
        model = PhishingDomain
        fields = ('id', 'url', 'domain_name', 'registration_date', 'is_phishing', 'overall_score', 
                 'content_analysis', 'behavior_analysis', 'ssl_analysis', 'ui_analysis', 'recent_logs')
    
    def get_recent_logs(self, obj):
        logs = DetectionLog.objects.filter(domain=obj).order_by('-detection_time')[:5]
        return DetectionLogSerializer(logs, many=True).data
