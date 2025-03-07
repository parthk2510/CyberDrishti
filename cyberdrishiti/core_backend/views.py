from rest_framework import generics
from .models import PhishingDomain
from .serializers import PhishingDomainSerializer
from .task import analyze_domain_task


class DomainDetectionAPI(generics.CreateAPIView):
    queryset = PhishingDomain.objects.all()
    serializer_class = PhishingDomainSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        analyze_domain_task.delay(instance.url)
