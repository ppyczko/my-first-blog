from django.contrib import admin

from .models import Category, Comment, Post, PostRecord, RelatedPost

admin.site.register([Category, Post, PostRecord, RelatedPost, Comment])
