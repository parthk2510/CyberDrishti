from django.contrib import admin
from .models import PhishingDomain, DetectionLog
# Register your models here.
admin.site.register(PhishingDomain)
admin.site.register(DetectionLog)
