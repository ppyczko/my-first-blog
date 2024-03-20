from django.contrib import admin
from .models import Post, PostRecord

admin.site.register([Post, PostRecord])
