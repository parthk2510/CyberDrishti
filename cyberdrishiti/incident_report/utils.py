import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO

def render_to_pdf(template_src, context_dict={}):
    """
    Generate a PDF file from an HTML template and context data
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None

def save_pdf(report_id, pdf_data):
    """
    Save the PDF data to a file in the media directory
    """
    # Create media directory if it doesn't exist
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    
    # Create a subdirectory for incident reports
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'incident_reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Define the file path
    file_path = os.path.join(reports_dir, f'incident_report_{report_id}.pdf')
    
    # Write the PDF data to the file
    with open(file_path, 'wb') as f:
        f.write(pdf_data)
    
    # Return the relative path to the file
    return os.path.join('incident_reports', f'incident_report_{report_id}.pdf') 