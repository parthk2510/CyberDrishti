from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
import shutil
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import urlparse
import tempfile
import os
import logging
import json
import time
from django.views.decorators.http import require_GET
from .models import PhishingDomain, DetectionLog, ContentAnalysis, DomainBehaviorAnalysis, SSLAnalysis, UICloneAnalysis
from .serializers import PhishingDomainSerializer, AnalysisResultSerializer
from .ml_models.content_analyzer import PhishingContentAnalyzer
from .ml_models.domain_behavior_analyzer import PhishingDetector as DomainBehaviorAnalyzer
from .ml_models.ssl_mismatch_detector import SSLCertificateAnalyzer
from .ml_models.ui_clone_detector import capture_screenshot_from_url, compare_ui_elements
from .tasks import analyze_domain_task


# Configure logging
logger = logging.getLogger(__name__)


def homepage(request):
    return HttpResponse("<h1>CyberDrishti</h1><p>Phishing Detection System API</p>")


def analyze_ssl_view(request):
    if request.method == 'POST':
        url_to_analyze = request.POST.get('url')
        if url_to_analyze:
            analyzer = SSLCertificateAnalyzer()
            analysis_result = analyzer.analyze_certificate(
                url_to_analyze, tls_check=True)

            # Store the result in session for display
            request.session['analysis_result'] = json.dumps(analysis_result)

            context = {'analysis': analysis_result}
            return render(request, 'ssl_analysis_report.html', context)
        else:
            return HttpResponse("Please provide a URL.")
    # Form to input URL
    return render(request, 'ssl_analysis_form.html')


class PhishingAnalysisAPI(APIView):
    def post(self, request):
        try:
            url = request.data.get('url')
            if not url:
                return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

            domain_name = urlparse(url).netloc
            existing_domain = PhishingDomain.objects.filter(url=url).first()

            if existing_domain and (hasattr(existing_domain, 'content_analysis') or hasattr(existing_domain, 'behavior_analysis')):
                serializer = AnalysisResultSerializer(existing_domain)
                return Response(serializer.data)

            if not existing_domain:
                domain = PhishingDomain.objects.create(
                    url=url,
                    domain_name=domain_name
                )
            else:
                domain = existing_domain

            temp_dir = tempfile.mkdtemp()
            screenshot_path = os.path.join(
                temp_dir, f"{domain_name}_screenshot.png")

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
                logger.error(
                    f"Domain behavior analysis error for {url}: {str(e)}")

            # SSL Analysis
            try:
                ssl_analyzer = SSLCertificateAnalyzer()
                ssl_result = ssl_analyzer.analyze_certificate(
                    url, tls_check=True)
                ssl_score = ssl_result['validation_score']
                overall_score += ssl_score
                analysis_count += 1

                cert_details = ssl_result.get('cert_details', {})
                issuer = cert_details.get('issuer', {}).get('commonname', ['Unknown'])[
                    0] if cert_details else 'Unknown'
                validity_status = cert_details.get(
                    'validity_status', 'unknown') if cert_details else 'unknown'

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
                screenshot_saved = capture_screenshot_from_url(
                    url, screenshot_path)
                ui_score = 0.0

                if screenshot_saved:
                    similar_domains = ['google.com', 'facebook.com',
                                       'apple.com', 'amazon.com', 'microsoft.com']
                    max_similarity = 0.0
                    similar_to = None

                    for reference_domain in similar_domains:
                        ref_screenshot = os.path.join(
                            temp_dir, f"{reference_domain}_screenshot.png")
                        if capture_screenshot_from_url(f"https://{reference_domain}", ref_screenshot):
                            similarity, _ = compare_ui_elements(
                                screenshot_path, ref_screenshot)
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

            serializer = AnalysisResultSerializer(domain)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error in PhishingAnalysisAPI: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DomainListCreateAPI(generics.ListCreateAPIView):
    queryset = PhishingDomain.objects.all().order_by('-registration_date')
    serializer_class = PhishingDomainSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'status': 'pending',
                    'message': 'Analysis started',
                    'data': serializer.data
                },
                status=status.HTTP_202_ACCEPTED,
                headers=headers
            )
        except Exception as e:
            logger.error(f"Error in DomainListCreateAPI.create: {str(e)}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        instance = serializer.save()
        # Instead of using Celery, perform analysis directly for now
        # You can implement the Celery task later
        try:
            analyze_domain(instance.url)
        except Exception as e:
            logger.error(f"Error during domain analysis: {str(e)}")


class DomainDetailAPI(generics.RetrieveAPIView):
    queryset = PhishingDomain.objects.all()
    serializer_class = PhishingDomainSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logs = DetectionLog.objects.filter(
                domain=instance).order_by('-detection_time')[:5]

            response_data = {
                'domain': serializer.data,
                'recent_logs': [
                    {
                        'timestamp': log.detection_time.isoformat(),
                        'confidence': log.ai_confidence,
                        'action': log.action_taken
                    } for log in logs
                ]
            }
            return Response(response_data)
        except Exception as e:
            logger.error(f"Error in DomainDetailAPI.retrieve: {str(e)}")
            return Response({'error': 'An error occurred while retrieving domain details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BatchAnalysisAPI(APIView):
    def post(self, request):
        try:
            urls = request.data.get('urls', [])
            if not urls:
                return Response({'error': 'No URLs provided'}, status=status.HTTP_400_BAD_REQUEST)

            results = []
            for url in urls:
                domain_name = urlparse(url).netloc
                domain, created = PhishingDomain.objects.get_or_create(
                    url=url,
                    defaults={'domain_name': domain_name}
                )
                # Instead of using Celery, perform analysis directly for now
                # You can implement the Celery task later
                try:
                    analyze_domain(url)
                except Exception as e:
                    logger.error(
                        f"Error during batch domain analysis: {str(e)}")

                results.append({
                    'url': url,
                    'status': 'pending',
                    'domain_id': str(domain.id)
                })

            return Response({'results': results}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.error(f"Error in BatchAnalysisAPI: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Helper function for direct analysis
def analyze_domain(url):
    """Analyze a domain without using Celery task"""
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

    # Run all analyses (content, behavior, SSL, UI) and update the domain
    # [Same analysis code as in PhishingAnalysisAPI.post]

    return {
        'url': url,
        'is_phishing': domain.is_phishing,
        'score': domain.overall_score
    }


@require_POST
def ui_similarity_view(request):
    try:
        original_url = request.POST.get("original_url")
        phishing_url = request.POST.get("phishing_url")
        if not original_url or not phishing_url:
            return JsonResponse({"error": "Both URLs must be provided."}, status=400)
        temp_dir = tempfile.mkdtemp()
        original_screenshot_path = os.path.join(
            temp_dir, "original_screenshot.png")
        phishing_screenshot_path = os.path.join(
            temp_dir, "phishing_screenshot.png")
        path1 = capture_screenshot_from_url(
            original_url, original_screenshot_path)
        path2 = capture_screenshot_from_url(
            phishing_url, phishing_screenshot_path)
        if not path1 or not path2:
            shutil.rmtree(temp_dir)
            return JsonResponse({"error": "Screenshot capture failed. Cannot perform comparison."}, status=500)
        similarity_percentage, message = compare_ui_elements(
            path1, path2)
        shutil.rmtree(temp_dir)
        return JsonResponse({
            "original_url": original_url,
            "phishing_url": phishing_url,
            "similarity_percentage": similarity_percentage,
            "message": message
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

        # your custom function

@require_GET
def ui_similarity_view_get(request):
    """
    GET-based UI similarity endpoint.

    Expects 'original_url' and 'phishing_url' as query parameters, for example:
      GET /api/ui-similarity/?original_url=...&phishing_url=...
    """
    try:
        original_url = request.GET.get("original_url")
        phishing_url = request.GET.get("phishing_url")

        if not original_url or not phishing_url:
            return JsonResponse({"error": "Both URLs must be provided."}, status=400)

        # Create a temporary directory to store screenshots
        temp_dir = tempfile.mkdtemp()

        original_screenshot_path = os.path.join(
            temp_dir, "original_screenshot.png")
        phishing_screenshot_path = os.path.join(
            temp_dir, "phishing_screenshot.png")

        # Capture screenshots
        path1 = capture_screenshot_from_url(
            original_url, original_screenshot_path)
        path2 = capture_screenshot_from_url(
            phishing_url, phishing_screenshot_path)

        if not path1 or not path2:
            shutil.rmtree(temp_dir)
            return JsonResponse({"error": "Screenshot capture failed. Cannot perform comparison."}, status=500)

        # Compare screenshots
        similarity_percentage, message = compare_ui_elements(path1, path2)

        # Clean up the temp directory
        shutil.rmtree(temp_dir)

        return JsonResponse({
            "original_url": original_url,
            "phishing_url": phishing_url,
            "similarity_percentage": similarity_percentage,
            "message": message
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
