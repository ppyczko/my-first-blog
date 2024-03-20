from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Post, PostRecord
from .forms import PostForm


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        queryset = (
            queryset.filter(published_date__lte=timezone.now())
            .order_by("published_date")
            .select_related("author")
        )
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        return super().get_queryset().select_related("author")


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        result = super().form_valid(form)
        return result

    def get_success_url(self) -> str:
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.published_date = timezone.now()
        result = super().form_valid(form)
        # We save a new register after modifying the post
        register = PostRecord()
        register.post = self.object
        register.user = self.object.author
        register.save()
        return result

    def get_success_url(self) -> str:
        return reverse("post_detail", kwargs={"pk": self.object.pk})


# Author views
class AuthorDetailView(DetailView):
    model = User
    template_name = "blog/author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object.__dict__)
        context["author_posts"] = self.object.records.all()
        return context
