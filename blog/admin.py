from django.contrib import admin

from .models import Post, PostRecord, RelatedPost, Comment

admin.site.register([Post, PostRecord, RelatedPost, Comment])
