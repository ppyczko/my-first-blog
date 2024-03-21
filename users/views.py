from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.urls import reverse


class LoginUserView(auth_views.LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    next_page = "blog-redirect"
    redirect_authenticated_user = True
