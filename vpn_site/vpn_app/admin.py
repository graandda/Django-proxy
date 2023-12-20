from django.contrib import admin
from .models import UserProfile, TrafficStatistic, Site

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(TrafficStatistic)
admin.site.register(Site)
