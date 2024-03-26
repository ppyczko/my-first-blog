from django.contrib import admin

from .models import Category, Comment, Post, PostRecord, RelatedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "published_date"]
    list_filter = ["title", "author", "category", "published_date"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "body", "created_date", "active"]
    list_filter = ["post", "author", "created_date", "active"]


@admin.register(PostRecord)
class PostRecordAdmin(admin.ModelAdmin):
    list_display = ["post", "user", "modified_date"]
    list_filter = ["post", "user", "modified_date"]
    date_hierarchy = "modified_date"


@admin.register(RelatedPost)
class RelatedPostAdmin(admin.ModelAdmin):
    list_display = ["main_post", "related_post"]
    list_filter = ["main_post", "related_post"]
