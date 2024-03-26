from django import template
from django.template.defaultfilters import stringfilter
from ..models import Post
from django.utils.safestring import mark_safe

register = template.Library()


@stringfilter
def format_author_name(value, arg):
    author = f"{value[0].capitalize()}. {arg.capitalize()}"
    return author


def last_posts(value):
    posts = Post.objects.filter(category=value).order_by("-published_date")[0:3]
    return posts


register.filter("format_author_name", format_author_name)
register.filter("last_posts", last_posts)
