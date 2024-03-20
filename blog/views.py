from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse

from .models import Post, PostRecord
from .forms import PostForm


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        return queryset.filter(published_date__lte=timezone.now()).order_by(
            "published_date"
        )


class PostDetailView(DetailView):
    model = Post


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
