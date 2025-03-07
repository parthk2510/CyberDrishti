from django.db import models


class PhishingDomain(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Investigation'),
        ('BLOCKED', 'Domain Blocked'),
        ('WHITELISTED', 'Legitimate Domain'),
    ]

    url = models.URLField(unique=True)
    registration_date = models.DateField(auto_now_add=True)
    registrar = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ssl_info = models.JSONField(null=True, blank=True)  # Allow null and blank
    screenshot_path = models.CharField(max_length=255, blank=True)
    threat_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.url} ({self.status})"


class DetectionLog(models.Model):
    domain = models.ForeignKey(PhishingDomain, on_delete=models.CASCADE)
    detection_time = models.DateTimeField(auto_now_add=True)
    ai_confidence = models.FloatField()
    action_taken = models.CharField(max_length=100)
    evidence = models.JSONField(blank=True, null=True)  # Allow null and blank

    class Meta:
        ordering = ['-detection_time']
