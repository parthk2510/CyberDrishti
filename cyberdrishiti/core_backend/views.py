from rest_framework import generics, status
from rest_framework.response import Response
from .models import PhishingDomain, DetectionLog
from .serializers import PhishingDomainSerializer
from .task import analyze_domain_task
from django.http import HttpResponse
import logging

# Configure logging
logger = logging.getLogger(__name__)


def homepage(request):
    return HttpResponse("<h1>Welcome to CyberDrishti!</h1><p>Phishing Detection System Backend API</p>")


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
        analyze_domain_task.delay(instance.url)


class DomainDetailAPI(generics.RetrieveAPIView):
    queryset = PhishingDomain.objects.all()
    serializer_class = PhishingDomainSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
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


class DomainDetectionAPI(generics.GenericAPIView):
    serializer_class = PhishingDomainSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            url = serializer.validated_data['url']

            # Check if domain already exists
            if PhishingDomain.objects.filter(url=url).exists():
                return Response(
                    {'error': 'This domain is already being analyzed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            domain = serializer.save()
            analyze_domain_task.delay(domain.url)

            return Response(
                {
                    'status': 'pending',
                    'message': 'Analysis started',
                    'domain_id': domain.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            logger.error(f"Error in DomainDetectionAPI.post: {str(e)}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
