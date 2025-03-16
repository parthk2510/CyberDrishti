from django.db import models
from django.utils import timezone
import uuid
from core_backend.models import PhishingDomain

class IncidentStatus(models.TextChoices):
    NEW = 'new', 'New'
    INVESTIGATING = 'investigating', 'Investigating'
    CONTAINED = 'contained', 'Contained'
    RESOLVED = 'resolved', 'Resolved'
    FALSE_POSITIVE = 'false_positive', 'False Positive'

class IncidentSeverity(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
    CRITICAL = 'critical', 'Critical'

class IncidentType(models.TextChoices):
    PHISHING = 'phishing', 'Phishing'
    MALWARE = 'malware', 'Malware'
    SOCIAL_ENGINEERING = 'social_engineering', 'Social Engineering'
    UNAUTHORIZED_ACCESS = 'unauthorized_access', 'Unauthorized Access'
    DATA_BREACH = 'data_breach', 'Data Breach'
    OTHER = 'other', 'Other'

class IncidentReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    incident_type = models.CharField(
        max_length=50,
        choices=IncidentType.choices,
        default=IncidentType.PHISHING
    )
    severity = models.CharField(
        max_length=20,
        choices=IncidentSeverity.choices,
        default=IncidentSeverity.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=IncidentStatus.choices,
        default=IncidentStatus.NEW
    )
    reported_by = models.CharField(max_length=255, null=True, blank=True)
    reported_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    affected_domain = models.ForeignKey(
        PhishingDomain, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='incidents'
    )
    auto_generated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-reported_at']
        
class IncidentAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='actions')
    action_taken = models.TextField()
    action_time = models.DateTimeField(default=timezone.now)
    action_by = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Action for {self.incident.title} at {self.action_time}"
    
    class Meta:
        ordering = ['-action_time']

class IncidentArtifact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(IncidentReport, on_delete=models.CASCADE, related_name='artifacts')
    name = models.CharField(max_length=255)
    artifact_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='incident_artifacts/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name 