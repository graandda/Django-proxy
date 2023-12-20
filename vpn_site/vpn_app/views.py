from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .forms import SiteForm, ProfileForm
import requests

from .models import Site, UserProfile, TrafficStatistic


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard_view(request):
    traffic_data = TrafficStatistic.objects.filter(user=request.user)
    return render(
        request,
        "profile/dashboard.html",
        {"user": request.user, "traffic_data": traffic_data},
    )


@login_required
def profile_view(request):

    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.userprofile)
    context = {"form": form}
    return render(request, "profile/profile.html", context=context)


def proxy_view(request, user_site_name, routes_on_original_site):

    original_site_url = f"{routes_on_original_site}"
    next_orginal_url = f"https://{original_site_url.split('//')[1]}"

    try:
        if request.method == "GET":
            response = requests.get(original_site_url)
        elif request.method == "POST":
            data = request.POST
            response = requests.post(original_site_url, data=data)
        else:
            return HttpResponse(status=405)

        custom_route = reverse(
            "proxy_view",
            kwargs={
                "user_site_name": user_site_name,
                "routes_on_original_site": next_orginal_url,
            },
        )

        modified_content = (
            response.content.decode()
            .replace(f'<a href="{next_orginal_url}', f'<a href="{custom_route}')
            .replace(
                f'<form action="{next_orginal_url}', f'<form action="{custom_route}'
            )
        )
        return render(request, "proxy/proxy_page.html", {"content": modified_content})

    except requests.RequestException as e:
        return render(request, "proxy/error_page.html", {"error_message": str(e)})


class UserSitesPageView(TemplateView):
    template_name = "profile/user_sites.html"


def get_site_list(request):
    context = {}
    context["sites"] = Site.objects.filter(user=request.user)
    return render(request, "profile/partial/site/site_list.html", context)


def add_site(request):
    context = {"form": SiteForm()}
    return render(request, "profile/partial/site/add_site.html", context)


def add_site_cancel(request):
    return HttpResponse()


def add_site_submit(request):
    context = {}
    form = SiteForm(request.POST)

    context["form"] = form
    context["is_edit_page"] = True
    if form.is_valid():
        site = form.save(commit=False)
        site.user = request.user
        context["site"] = form.save()
    else:
        return render(request, "profile/partial/site/add_site.html", context)
    return render(request, "profile/partial/site/site_row.html", context)


def edit_site(request, site_pk):
    site = Site.objects.get(pk=site_pk)
    context = {}
    context["site"] = site
    context["form"] = SiteForm(
        initial={
            "name": site.name,
            "url": site.url,
        }
    )
    context["is_edit_page"] = True
    return render(request, "profile/partial/site/edit_site.html", context)


@require_http_methods(["GET", "POST"])
def edit_site_submit(request, site_pk):
    context = {}
    site = Site.objects.get(pk=site_pk)
    context["site"] = site
    context["is_edit_page"] = True
    if request.method == "POST":
        form = SiteForm(request.POST, instance=site)
        print("1")
        if form.is_valid():

            form.save()
        else:
            return render(request, "profile/partial/site/edit_site.html", context)

    return render(request, "profile/partial/site/site_row.html", context)


def delete_site(site_pk):
    site = Site.objects.get(pk=site_pk)
    site.delete()
    return HttpResponse()
