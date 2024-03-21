from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    AuthorDetailView,
    CategoryDetailView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "post/category/<str:category>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author_detail"),
]
