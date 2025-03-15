from celery import shared_task
from urllib.parse import urlparse
import tempfile
import os
import logging
import time

logger = logging.getLogger(__name__)

@shared_task
def analyze_domain_task(url):
    try:
        from .models import PhishingDomain, ContentAnalysis, DomainBehaviorAnalysis, SSLAnalysis, UICloneAnalysis, DetectionLog
        from .ml_models.content_analyzer import PhishingContentAnalyzer
        from .ml_models.domain_behavior_analyzer import PhishingDetector as DomainBehaviorAnalyzer
        from .ml_models.ssl_mismatch_detector import SSLCertificateAnalyzer
        from .ml_models.ui_clone_detector import capture_screenshot_from_url, compare_ui_elements
        
        domain_name = urlparse(url).netloc
        
        try:
            domain = PhishingDomain.objects.get(url=url)
        except PhishingDomain.DoesNotExist:
            domain = PhishingDomain.objects.create(
                url=url,
                domain_name=domain_name
            )
        
        temp_dir = tempfile.mkdtemp()
        screenshot_path = os.path.join(temp_dir, f"{domain_name}_screenshot.png")
        
        overall_score = 0.0
        analysis_count = 0
        
        # Content Analysis
        try:
            content_analyzer = PhishingContentAnalyzer(url)
            content_score = content_analyzer.calculate_threat_score()
            overall_score += content_score / 20.0  # Normalize to 0-1
            analysis_count += 1
            
            ContentAnalysis.objects.update_or_create(
                domain=domain,
                defaults={
                    'ssl_valid': content_analyzer.ssl_valid,
                    'domain_age': content_analyzer.domain_age,
                    'suspicious_elements': content_analyzer.suspicious_elements,
                    'score': content_score / 20.0,
                }
            )
        except Exception as e:
            logger.error(f"Content analysis error for {url}: {str(e)}")
        
        # Domain Behavior Analysis
        try:
            behavior_analyzer = DomainBehaviorAnalyzer(domain_name)
            behavior_analyzer.check_dns()
            behavior_score = behavior_analyzer.calculate_threat_score()
            overall_score += behavior_score / 10.0  # Normalize to 0-1
            analysis_count += 1
            
            DomainBehaviorAnalysis.objects.update_or_create(
                domain=domain,
                defaults={
                    'mx_exists': behavior_analyzer.mx_exists,
                    'spf_exists': behavior_analyzer.spf_exists,
                    'dmarc_exists': behavior_analyzer.dmarc_exists,
                    'a_record_count': behavior_analyzer.a_record_count,
                    'domain_age_score': behavior_analyzer.domain_age_score,
                    'score': behavior_score / 10.0,
                }
            )
        except Exception as e:
            logger.error(f"Domain behavior analysis error for {url}: {str(e)}")
        
        # SSL Analysis
        try:
            ssl_analyzer = SSLCertificateAnalyzer()
            ssl_result = ssl_analyzer.analyze_certificate(url, tls_check=True)
            ssl_score = ssl_result['validation_score']
            overall_score += ssl_score
            analysis_count += 1
            
            cert_details = ssl_result.get('cert_details', {})
            issuer = cert_details.get('issuer', {}).get('commonname', ['Unknown'])[0] if cert_details else 'Unknown'
            validity_status = cert_details.get('validity_status', 'unknown') if cert_details else 'unknown'
            
            SSLAnalysis.objects.update_or_create(
                domain=domain,
                defaults={
                    'certificate_valid': ssl_result.get('certificate_valid', False),
                    'hostname_match': ssl_result.get('hostname_match', False),
                    'tls_valid': ssl_result.get('tls_valid', False),
                    'issuer': issuer,
                    'validity_status': validity_status,
                    'score': ssl_score,
                }
            )
        except Exception as e:
            logger.error(f"SSL analysis error for {url}: {str(e)}")
        
        # UI Clone Analysis
        try:
            screenshot_saved = capture_screenshot_from_url(url, screenshot_path)
            ui_score = 0.0
            
            if screenshot_saved:
                similar_domains = ['google.com', 'facebook.com', 'apple.com', 'amazon.com', 'microsoft.com']
                max_similarity = 0.0
                similar_to = None
                
                for reference_domain in similar_domains:
                    ref_screenshot = os.path.join(temp_dir, f"{reference_domain}_screenshot.png")
                    if capture_screenshot_from_url(f"https://{reference_domain}", ref_screenshot):
                        similarity, _ = compare_ui_elements(screenshot_path, ref_screenshot)
                        if similarity > max_similarity:
                            max_similarity = similarity
                            similar_to = reference_domain
                
                ui_score = max_similarity / 100.0
                overall_score += ui_score
                analysis_count += 1
                
                UICloneAnalysis.objects.update_or_create(
                    domain=domain,
                    defaults={
                        'similar_to': similar_to,
                        'screenshot_path': screenshot_path,
                        'similarity_score': ui_score,
                    }
                )
        except Exception as e:
            logger.error(f"UI clone analysis error for {url}: {str(e)}")
        
        # Calculate overall score and update domain
        if analysis_count > 0:
            final_score = overall_score / analysis_count
            is_phishing = final_score > 0.6  # Threshold for phishing classification
            
            domain.overall_score = final_score
            domain.is_phishing = is_phishing
            domain.save()
            
            DetectionLog.objects.create(
                domain=domain,
                ai_confidence=final_score,
                action_taken="Flagged as phishing" if is_phishing else "Marked as safe"
            )
        
        return {
            'url': url,
            'is_phishing': domain.is_phishing,
            'score': domain.overall_score
        }
    
    except Exception as e:
        logger.error(f"Error in analyze_domain_task for {url}: {str(e)}")
        return {'error': str(e)} 