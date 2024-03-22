from django.contrib import admin

from .models import Post, PostRecord, RelatedPost

admin.site.register([Post, PostRecord, RelatedPost])
