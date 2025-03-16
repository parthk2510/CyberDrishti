from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import IncidentReportForm
from .models import IncidentReport, IncidentAction, IncidentArtifact
from .utils import render_to_pdf, save_pdf
import os
import logging
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .serializers import (
    IncidentReportSerializer, 
    IncidentReportCreateSerializer,
    IncidentReportUpdateSerializer,
    IncidentActionSerializer, 
    IncidentArtifactSerializer
)
from core_backend.models import PhishingDomain

class IncidentReportViewSet(viewsets.ModelViewSet):
    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer

# Set up logging
logger = logging.getLogger(__name__)

def incident_report_view(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            try:
                # Save the form data
                incident_report = form.save()
                
                # Get the incident types that were selected
                incident_types_selected = []
                incident_types_dict = {}
                
                for incident_code, incident_label in form.INCIDENT_TYPES:
                    if incident_report.incident_types.get(incident_code):
                        incident_types_selected.append(incident_label)
                        incident_types_dict[incident_code] = True
                    else:
                        incident_types_dict[incident_code] = False
                
                # Prepare context for email and PDF
                context = {
                    'report': incident_report,
                    'incident_types': incident_types_selected,
                    'incident_types_dict': incident_types_dict,
                    'INCIDENT_TYPES': form.INCIDENT_TYPES,
                }
                
                # Generate PDF
                pdf_data = render_to_pdf('incident_report/pdf/report_template.html', context)
                
                if pdf_data:
                    # Save PDF to file
                    pdf_file_path = save_pdf(incident_report.id, pdf_data)
                    pdf_file_full_path = os.path.join(settings.MEDIA_ROOT, pdf_file_path)
                    
                    # Render email content
                    html_message = render_to_string('incident_report/email_template.html', context)
                    plain_message = strip_tags(html_message)
                    
                    # Check if email settings are configured
                    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                        messages.warning(request, 'Email settings not configured. PDF generated but email not sent.')
                        logger.warning('Email settings not configured. Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env file.')
                    else:
                        try:
                            # Create email message
                            subject = f'Incident Report #{incident_report.id}'
                            email = EmailMessage(
                                subject=subject,
                                body=html_message,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[settings.EMAIL_RECIPIENT],
                            )
                            
                            # Add HTML content
                            email.content_subtype = "html"
                            
                            # Attach PDF
                            with open(pdf_file_full_path, 'rb') as f:
                                email.attach(f'incident_report_{incident_report.id}.pdf', f.read(), 'application/pdf')
                            
                            # Send email
                            email.send(fail_silently=False)
                            messages.success(request, 'Incident report submitted successfully. Thank you!')
                        except Exception as e:
                            logger.error(f'Email sending failed: {str(e)}')
                            messages.warning(request, f'Report saved but email notification failed: {str(e)}')
                else:
                    messages.warning(request, 'Report saved but PDF generation failed.')
            except Exception as e:
                logger.error(f'Error processing form: {str(e)}')
                messages.error(request, f'An error occurred while processing your report: {str(e)}')
            
            return redirect('incident_report_success')
    else:
        form = IncidentReportForm()
    
    return render(request, 'incident_report/incident_form.html', {'form': form})

def incident_report_success(request):
    return render(request, 'incident_report/success.html')

def incident_dashboard(request):
    """Render the incident response dashboard"""
    incidents = IncidentReport.objects.all().order_by('-reported_at')[:10]
    return render(request, 'incident_report/dashboard.html', {
        'incidents': incidents,
    })

class IncidentReportListCreateView(generics.ListCreateAPIView):
    queryset = IncidentReport.objects.all().order_by('-reported_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IncidentReportCreateSerializer
        return IncidentReportSerializer
    
    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Incident report created: {instance.title}")
            
            # Log the creation as an action
            IncidentAction.objects.create(
                incident=instance,
                action_taken="Incident report created",
                action_by=instance.reported_by or "System"
            )
            
            return instance
        except Exception as e:
            logger.error(f"Error creating incident report: {str(e)}")
            raise

class IncidentReportDetailView(generics.RetrieveUpdateAPIView):
    queryset = IncidentReport.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return IncidentReportUpdateSerializer
        return IncidentReportSerializer
    
    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        updated_instance = serializer.save()
        
        # Check if status changed and record it as an action
        if old_status != updated_instance.status:
            IncidentAction.objects.create(
                incident=updated_instance,
                action_taken=f"Status changed from {old_status} to {updated_instance.status}",
                action_by=self.request.user.username if self.request.user.is_authenticated else "System"
            )
            
            # If resolved, set resolved_at
            if updated_instance.status == 'resolved' and not updated_instance.resolved_at:
                updated_instance.resolved_at = timezone.now()
                updated_instance.save()
        
        return updated_instance

class IncidentActionListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentActionSerializer
    
    def get_queryset(self):
        incident_id = self.kwargs.get('incident_id')
        return IncidentAction.objects.filter(incident_id=incident_id).order_by('-action_time')
    
    def perform_create(self, serializer):
        incident_id = self.kwargs.get('incident_id')
        incident = get_object_or_404(IncidentReport, id=incident_id)
        serializer.save(incident=incident)

class IncidentArtifactListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentArtifactSerializer
    
    def get_queryset(self):
        incident_id = self.kwargs.get('incident_id')
        return IncidentArtifact.objects.filter(incident_id=incident_id)
    
    def perform_create(self, serializer):
        incident_id = self.kwargs.get('incident_id')
        incident = get_object_or_404(IncidentReport, id=incident_id)
        serializer.save(incident=incident)

class AutoReportPhishingIncident(APIView):
    """API to automatically create an incident report from a phishing domain"""
    
    def post(self, request, *args, **kwargs):
        try:
            domain_id = request.data.get('domain_id')
            if not domain_id:
                return Response(
                    {'error': 'domain_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the phishing domain
            try:
                domain = PhishingDomain.objects.get(id=domain_id)
            except PhishingDomain.DoesNotExist:
                return Response(
                    {'error': 'Domain not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if this domain already has an incident
            if IncidentReport.objects.filter(affected_domain=domain).exists():
                return Response(
                    {'message': 'An incident already exists for this domain', 
                     'incident_id': str(IncidentReport.objects.filter(affected_domain=domain).first().id)}, 
                    status=status.HTTP_200_OK
                )
            
            # Create a new incident report
            severity = 'high' if domain.overall_score and domain.overall_score > 0.7 else 'medium'
            
            incident = IncidentReport.objects.create(
                title=f"Potential phishing detected: {domain.domain_name}",
                description=f"Automatic incident report for potential phishing site. Threat score: {domain.overall_score or 'Unknown'}",
                incident_type='phishing',
                severity=severity,
                affected_domain=domain,
                auto_generated=True,
                reported_by="Automated System"
            )
            
            # Create initial action
            IncidentAction.objects.create(
                incident=incident,
                action_taken="Incident automatically generated from phishing detection system",
                action_by="Automated System"
            )
            
            logger.info(f"Auto-created incident report for domain {domain.domain_name}")
            
            return Response({
                'message': 'Incident report created successfully',
                'incident_id': str(incident.id)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error in AutoReportPhishingIncident: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 