from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    categories = (
        ("stories", "Stories"),
        ("films", "Films"),
        ("books", "Books"),
        ("sports", "Sports"),
        ("fashion", "Fashion"),
        ("politics", "Politics"),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.CharField(max_length=15, choices=categories, default="stories")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class PostRecord(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.post} - {self.user}"
