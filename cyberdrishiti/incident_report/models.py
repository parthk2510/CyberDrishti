from django.db import models
from django.utils import timezone

class IncidentReport(models.Model):
    # Reporter Information
    REPORTER_TYPE_CHOICES = [
        ('affected_entity', 'The affected entity'),
        ('reporting_other', 'Reporting incident affecting other entity'),
    ]
    
    REPORTER_IDENTITY_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    
    reporter_type = models.CharField(max_length=20, choices=REPORTER_TYPE_CHOICES)
    reporter_identity = models.CharField(max_length=20, choices=REPORTER_IDENTITY_CHOICES)
    name_role = models.CharField(max_length=255, verbose_name="Name & Role/Title")
    organization_name = models.CharField(max_length=255, blank=True, verbose_name="Organization name (if any)")
    contact_no = models.CharField(max_length=50, verbose_name="Contact No.")
    email = models.EmailField()
    address = models.TextField()
    
    # Basic Incident Details
    affected_entity = models.CharField(max_length=255, blank=True, 
                                      verbose_name="Affected entity (if not same as reporting entity)")
    
    # Incident Type (stored as JSON)
    incident_types = models.JSONField(default=dict)
    other_incident_details = models.TextField(blank=True)
    
    # Critical Information
    is_critical = models.CharField(max_length=5, choices=[('Yes', 'Yes'), ('No', 'No')],
                                  verbose_name="Is the affected system/network critical to the organization's mission?")
    critical_details = models.TextField(blank=True, verbose_name="Brief details")
    
    # System Information
    system_info = models.TextField(verbose_name="Basic Information of Affected System")
    domain_url = models.CharField(max_length=255, blank=True, verbose_name="Domain/URL")
    ip_address = models.CharField(max_length=50, blank=True, verbose_name="IP Address")
    operating_system = models.CharField(max_length=100, blank=True, verbose_name="Operating System")
    make_model = models.CharField(max_length=255, blank=True, verbose_name="Make/Model/Cloud details")
    app_details = models.TextField(blank=True, verbose_name="Affected Application details (if any)")
    location = models.CharField(max_length=255, blank=True, 
                               verbose_name="Location of affected system (including City, Region & Country)")
    isp_info = models.CharField(max_length=255, blank=True, verbose_name="Network and name of ISP")
    
    # Incident Description
    incident_description = models.TextField(verbose_name="Brief description of Incident")
    occurrence_date = models.DateTimeField(blank=True, null=True, verbose_name="Occurrence date & time")
    detection_date = models.DateTimeField(blank=True, null=True, verbose_name="Detection date & time")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Incident Report {self.id} - {self.name_role}" 