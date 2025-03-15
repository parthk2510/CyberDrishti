from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import IncidentReportForm
from .models import IncidentReport
from .utils import render_to_pdf, save_pdf
import os
import logging
from rest_framework import viewsets
from .serializers import IncidentReportSerializer

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