from celery import shared_task
from .models import PhishingDomain, DetectionLog
from .services.detection_service import PhishingDetector


@shared_task
def analyze_domain_task(url):
    detector = PhishingDetector()
    result = detector.analyze_domain(url)

    domain, created = PhishingDomain.objects.update_or_create(
        url=url,
        defaults={
            'threat_score': result['threat_score'],
            # Use get to avoid KeyError if 'ssl_info' is missing
            'ssl_info': result['features'].get('ssl_info', None)
        }
    )

    DetectionLog.objects.create(
        domain=domain,
        ai_confidence=result['threat_score'],
        action_taken='Pending Review',
        evidence=result['features']
    )

    if result['threat_score'] > 0.85:
        domain.status = 'BLOCKED'
        domain.save()
        # Trigger takedown workflow (to be implemented later)

    return domain.id
