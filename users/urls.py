from django.urls import path
from .views import LoginUserView, LogoutUser, SignUpUser
from blog.urls import PostListView

app_name = "users"

urlpatterns = [
    path("", PostListView.as_view(), name="blog-redirect"),
    path("accounts/login/", LoginUserView.as_view(), name="login"),
    path("accounts/logout", LogoutUser.as_view(), name="logout"),
    path("accounts/signup/", SignUpUser.as_view(), name="signup"),
]
