from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone, translation
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from extra_views import (
    ModelFormSetView,
    InlineFormSetFactory,
    CreateWithInlinesView,
    UpdateWithInlinesView,
)
from django.core.exceptions import ValidationError
from django.forms import BaseModelFormSet

from .filters import PostFilter
from .forms import PostForm, CommentForm
from .models import Post, PostRecord, Comment, Category


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
            .order_by("-published_date")
            .select_related("author", "category")
        )
        print(translation)
        return queryset


# Formsets
class PostBaseFormSet(BaseModelFormSet):

    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            author = form.cleaned_data.get("author")
            print(author, self.kwargs["user"])
            if author != self.kwargs["user"]:
                raise ValidationError("The users must be the same")


class PostFormSetview(ModelFormSetView):
    model = Post
    fields = ("title", "category", "text")
    template_name = "blog/post_formset.html"
    factory_kwargs = {"extra": 0}
    formset_class = PostBaseFormSet

    # def get_formset_kwargs(self):
    #     kwargs = super(PostFormSetview, self).get_formset_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse("blog:post_list")


# Ex 2
class PostInline(InlineFormSetFactory):
    model = Post
    fields = ("title", "text")
    factory_kwargs = {"extra": 0, "can_order": False, "can_delete": False}


class EditCategoryPosts(UpdateWithInlinesView):
    model = Category
    inlines = [PostInline]
    template_name = "blog/category_formset.html"
    fields = ("category",)

    def get_success_url(self):
        return reverse("blog:post_list")


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = self.object.posts_related.all()
        context["comment_form"] = CommentForm
        context["comments"] = self.object.comments.all().select_related("author")
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        result = super().form_valid(form)
        return result

    def get_success_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


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
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


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
    context_object_name = "posts_by_category"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.kwargs)
        category = Category.objects.get(category=self.kwargs["category"])
        queryset = Post.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.created_date = timezone.now()
        if "parent" in self.kwargs:
            form.instance.parent = Comment.objects.get(pk=self.kwargs["parent"])
        result = super().form_valid(form)
        return result

    def get_success_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})
