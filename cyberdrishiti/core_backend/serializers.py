# File: cyberdrishiti/core_backend/serializers.py
from rest_framework import serializers
from .models import PhishingDomain


class PhishingDomainSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PhishingDomain
        fields = [
            'id', 'url', 'status', 'threat_score',
            'registration_date', 'registrar'
        ]
        read_only_fields = [
            'status', 'threat_score', 'registration_date',
            'registrar', 'id'
        ]
