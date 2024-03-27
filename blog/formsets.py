from django.forms import modelformset_factory
from .models import Post

PostFormSet = modelformset_factory(
    Post, fields=("author", "title", "category", "text"), extra=3
)
