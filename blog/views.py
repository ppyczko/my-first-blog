from typing import Any

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import PostForm
from .models import Post, PostRecord
from .filters import PostFilter


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class PostListView(LoginRequiredMixin, FilteredListView):
    model = Post
    paginate_by = 10
    filterset_class = PostFilter

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


class AuthorDetailView(DetailView):
    model = User
    template_name = "blog/author_detail.html"
    context_object_name = "author"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_posts"] = self.object.post_set.all()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = "blog/category_detail.html"
    pk_url_kwarg = "category"
    context_object_name = "posts_by_category"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Post.objects.filter(category=self.kwargs["category"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        return context
