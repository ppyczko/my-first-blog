from django.urls import path
from .views import LoginUserView
from blog.urls import PostListView

urlpatterns = [
    path("", PostListView.as_view(), name="blog-redirect"),
    path(
        "accounts/login/",
        LoginUserView.as_view(),
    ),
]
