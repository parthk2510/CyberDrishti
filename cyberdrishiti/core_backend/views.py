from django.http import HttpResponse
from rest_framework import generics
from .models import PhishingDomain
from .serializers import PhishingDomainSerializer
from .task import analyze_domain_task


def homepage(request):
    return HttpResponse("<h1>Welcome to CyberDrishti!</h1><p>Phishing Detection System Backend API</p>")


class DomainDetectionAPI(generics.CreateAPIView):
    queryset = PhishingDomain.objects.all()
    serializer_class = PhishingDomainSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        analyze_domain_task.delay(instance.url)


class DomainDetailAPI(generics.RetrieveAPIView):  # New View
    queryset = PhishingDomain.objects.all()
    serializer_class = PhishingDomainSerializer
    lookup_field = 'pk'  # Use primary key to retrieve specific domain
