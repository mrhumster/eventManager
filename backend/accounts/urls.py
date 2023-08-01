from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name='index'),
    path("logout", views.logout_view, name="logout"),
    path("signin", views.signin_view, name="signin"),
    path("profile", views.profile_view, name="profile"),
    path("forgot_password", views.forgot_password_view, name="forgot-password"),
    path("change_password", views.change_password_view, name="change-password"),
    path("profile/<str:username>", views.userprofile_view, name="user_profile"),
    path("settings", views.settings_view, name="settings"),
    path("delete", views.delete_view, name="delete"),
    path("update", views.update_view, name="update"),
    path("email_verified", views.email_verified_view, name="email-verified"),
    path("<uuid:token>/", views.confirm_view, name="confirm")
]
