from django import forms
from .models import UserProfile, Site


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "city",
            "birthdate",
        ]


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            "name",
            "url",
        ]
