from django import forms
from django.utils import timezone
from .models import IncidentReport

class IncidentReportForm(forms.ModelForm):
    # Define incident type choices
    INCIDENT_TYPES = [
        ('targeted_scanning', 'Targeted scanning/probing of critical networks/systems'),
        ('compromise_systems', 'Compromise of critical systems/information'),
        ('unauthorised_access', 'Unauthorised access of IT systems/data'),
        ('defacement_intrusion', 'Defacement or intrusion into the website'),
        ('malicious_code', 'Malicious code attacks'),
        ('attack_servers', 'Attack on servers such as Database, Mail and DNS and network devices such as Routers'),
        ('identity_theft', 'Identity Theft, spoofing and phishing attacks'),
        ('dos_ddos', 'DoS/DDoS attacks'),
        ('attacks_critical', 'Attacks on critical infrastructure, SCADA and operational technology systems and Wireless networks'),
        ('attacks_application', 'Attacks on application such as E-Governance, E-Commerce etc.'),
        ('data_breach', 'Data Breach'),
        ('data_leak', 'Data Leak'),
        ('attacks_iot', 'Attacks on Internet of Things (IoT) devices and associated systems, networks, software, servers'),
        ('attacks_digital', 'Attacks or incident affecting Digital Payment services'),
        ('attacks_mobile', 'Attacks through Malicious mobile Apps'),
        ('unauthorised_social', 'Unauthorised access to social media accounts'),
        ('attacks_cloud', 'Attacks or malicious/ suspicious activities affecting Cloud computing systems/servers/software/applications'),
        ('attacks_systems', 'Attacks or malicious/suspicious activities affecting systems/ servers/ networks/ software/ applications related to Big Data, Block chain, virtual assets, virtual banking, custodian wallet, Robotics, 3D and 4D Printing, additive manufacturing, Drones'),
        ('attacks_ai', 'Attacks or malicious/ suspicious activities affecting systems/ servers/networks/ applications related to Artificial intelligence and Machine Learning'),
        ('other', 'Other (Please Specify)'),
    ]
    
    # Create a checkbox for each incident type
    for incident_code, incident_label in INCIDENT_TYPES:
        locals()[incident_code] = forms.BooleanField(
            label=incident_label,
            required=False,
        )
    
    # Add date-time fields with widgets
    occurrence_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )
    
    detection_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )
    
    class Meta:
        model = IncidentReport
        exclude = ['incident_types', 'created_at', 'updated_at']
        widgets = {
            'reporter_type': forms.RadioSelect(),
            'reporter_identity': forms.RadioSelect(),
            'is_critical': forms.RadioSelect(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'system_info': forms.Textarea(attrs={'rows': 3}),
            'critical_details': forms.Textarea(attrs={'rows': 2}),
            'app_details': forms.Textarea(attrs={'rows': 2}),
            'incident_description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Collect all incident types that were checked
        incident_types = {}
        for incident_code, _ in self.INCIDENT_TYPES:
            if cleaned_data.get(incident_code):
                incident_types[incident_code] = True
        
        # If "other" is selected, make sure other_incident_details is provided
        if incident_types.get('other') and not cleaned_data.get('other_incident_details'):
            self.add_error('other_incident_details', 'Please provide details for the "Other" incident type.')
        
        # Store the incident types in the JSON field
        self.cleaned_data['incident_types'] = incident_types
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save the incident types to the JSON field
        instance.incident_types = self.cleaned_data['incident_types']
        
        if commit:
            instance.save()
        
        return instance 