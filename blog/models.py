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
    related_posts = models.ManyToManyField(
        to="self",
        symmetrical=False,
        blank=True,
        through="RelatedPost",
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class RelatedPost(models.Model):
    main_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="posts_related"
    )
    related_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="posts_main"
    )

    def __str__(self):
        return f"Main: {self.main_post.title} - Related: {self.related_post.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "main_post", "related_post", name="unique_mainpost_relatedpost"
            )
        ]


class PostRecord(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.post} - {self.user}"
