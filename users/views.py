from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import LoginForm, SignUpForm


class LoginUserView(auth_views.LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    next_page = "blog:post_list"
    redirect_authenticated_user = True


class LogoutUser(auth_views.LogoutView):
    template_name = "users/logout.html"


class SignUpUser(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("blog:post_list")
    template_name = "users/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("blog:post_list")
        return super().get(request, *args, **kwargs)

    # Automatic login after signup
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PasswordReset(auth_views.PasswordResetView):
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"
