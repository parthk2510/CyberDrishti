from rest_framework import serializers
from .models import PhishingDomain


class PhishingDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhishingDomain
        fields = ['id', 'url', 'status', 'threat_score']
        read_only_fields = ['status', 'threat_score']
