from django.db import models
from django.utils import timezone
import uuid


class SSLAnalysisResult(models.Model):
    url = models.TextField(primary_key=True)
    timestamp = models.DateTimeField()
    certificate_valid = models.BooleanField()
    hostname_match = models.BooleanField()
    tls_valid = models.BooleanField()
    validation_score = models.FloatField()
    error = models.TextField(blank=True, null=True)
    cert_details_json = models.TextField()  # Store JSON as text

    def __str__(self):
        return f"SSL Analysis for {self.url} - Score: {self.validation_score}"
    
class PhishingDomain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=255)
    domain_name = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_phishing = models.BooleanField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.url

class ContentAnalysis(models.Model):
    domain = models.OneToOneField(PhishingDomain, on_delete=models.CASCADE, related_name='content_analysis')
    ssl_valid = models.BooleanField(default=False)
    domain_age = models.IntegerField(default=0)
    suspicious_elements = models.IntegerField(default=0)
    forms_with_password = models.BooleanField(default=False)
    suspicious_url_structure = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

class DomainBehaviorAnalysis(models.Model):
    domain = models.OneToOneField(PhishingDomain, on_delete=models.CASCADE, related_name='behavior_analysis')
    mx_exists = models.BooleanField(default=False)
    spf_exists = models.BooleanField(default=False)
    dmarc_exists = models.BooleanField(default=False)
    a_record_count = models.IntegerField(default=0)
    domain_age_score = models.IntegerField(default=0)
    traffic_spike = models.BooleanField(default=False)
    unusual_geolocations = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

class SSLAnalysis(models.Model):
    domain = models.OneToOneField(PhishingDomain, on_delete=models.CASCADE, related_name='ssl_analysis')
    certificate_valid = models.BooleanField(default=False)
    hostname_match = models.BooleanField(default=False)
    tls_valid = models.BooleanField(default=False)
    issuer = models.CharField(max_length=255, null=True, blank=True)
    validity_status = models.CharField(max_length=20, null=True, blank=True)
    score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

class UICloneAnalysis(models.Model):
    domain = models.OneToOneField(PhishingDomain, on_delete=models.CASCADE, related_name='ui_analysis')
    similar_to = models.CharField(max_length=255, null=True, blank=True)
    screenshot_path = models.CharField(max_length=255, null=True, blank=True)
    similarity_score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

class DetectionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.ForeignKey(PhishingDomain, on_delete=models.CASCADE, related_name='logs')
    detection_time = models.DateTimeField(default=timezone.now)
    ai_confidence = models.FloatField()
    action_taken = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.domain.url} - {self.detection_time}"
