from django.urls import path
from django.views.generic import RedirectView

from .views import (
    register_view,
    dashboard_view,
    profile_view,
    proxy_view,
    UserSitesPageView,
    get_site_list,
    add_site,
    add_site_submit,
    add_site_cancel,
    delete_site,
    edit_site,
    edit_site_submit,
)
from django.contrib.auth import views as auth_views

urlpatterns = (
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),
    path("register/", register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("sites/", UserSitesPageView.as_view(), name="sites"),
    path("get_site_list", get_site_list, name="get_site_list"),
    path("add_site", add_site, name="add_site"),
    path("add_site_submit", add_site_submit, name="add_site_submit"),
    path("add_site_cancel", add_site_cancel, name="add_site_cancel"),
    path("<int:site_pk>/delete_site", delete_site, name="delete_site"),
    path("<int:site_pk>/edit_site", edit_site, name="edit_site"),
    path("<int:site_pk>/edit_site_submit", edit_site_submit, name="edit_site_submit"),
    path(
        "proxy/<str:user_site_name>/<path:routes_on_original_site>/",
        proxy_view,
        name="proxy_view",
    ),
)
