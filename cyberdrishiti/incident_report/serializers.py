from rest_framework import serializers
from .models import IncidentReport, IncidentAction, IncidentArtifact
from core_backend.serializers import PhishingDomainSerializer

class IncidentActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentAction
        fields = '__all__'

class IncidentArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentArtifact
        fields = '__all__'

class IncidentReportSerializer(serializers.ModelSerializer):
    actions = IncidentActionSerializer(many=True, read_only=True)
    artifacts = IncidentArtifactSerializer(many=True, read_only=True)
    affected_domain_details = serializers.SerializerMethodField()
    
    class Meta:
        model = IncidentReport
        fields = '__all__'
    
    def get_affected_domain_details(self, obj):
        if obj.affected_domain:
            from core_backend.serializers import PhishingDomainSerializer
            return PhishingDomainSerializer(obj.affected_domain).data
        return None

class IncidentReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = ('title', 'description', 'incident_type', 'severity', 'reported_by', 'affected_domain')
        
class IncidentReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = ('title', 'description', 'incident_type', 'severity', 'status')