from django.urls import path

from .views import (
    LoginUserView,
    LogoutUser,
    SignUpUser,
    PasswordReset,
    PasswordResetDone,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from blog.urls import PostListView

app_name = "users"

urlpatterns = [
    path("accounts/login/", LoginUserView.as_view(), name="login"),
    path("accounts/logout", LogoutUser.as_view(), name="logout"),
    path("accounts/signup/", SignUpUser.as_view(), name="signup"),
    path("accounts/password_reset/", PasswordReset.as_view(), name="password_reset"),
    path(
        "accounts/password_reset/done/",
        PasswordResetDone.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
