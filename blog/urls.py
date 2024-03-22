from django.urls import path
from . import views
from .models import Post
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    AuthorDetailView,
    CategoryListView,
)
from users.views import LoginUserView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "post/category/<str:category>/",
        CategoryListView.as_view(),
        name="category_detail",
    ),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author_detail"),
]
