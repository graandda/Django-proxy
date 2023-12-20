from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, max_length=500)
    city = models.CharField(null=True, blank=True, max_length=50)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.url}"


class TrafficStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0)
    data_uploaded = models.IntegerField(default=0)
    data_downloaded = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.site}"
