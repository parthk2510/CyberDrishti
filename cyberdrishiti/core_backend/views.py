from django.http import HttpResponse
from rest_framework import generics
from .models import PhishingDomain
from .serializers import PhishingDomainSerializer
from .task import analyze_domain_task
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


def homepage(request):
    return HttpResponse("<h1>Welcome to CyberDrishti!</h1><p>Phishing Detection System Backend API</p>")


def default_homepage(request):
    return render(request, 'homepage.html')


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


@csrf_exempt
@api_view(['POST'])
def DomainDetectionAPI(request):
    # Your logic for saving the domain and triggering the Celery task
    # (For example, serializer.save() and analyze_domain_task.delay(instance.url))
    ...
