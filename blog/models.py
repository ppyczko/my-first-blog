from django.db import models
from django.conf import settings
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
    category = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, null=True, blank=True
    )
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


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["created_date"]

    def __str__(self):
        return "Comment on {} by {}".format(self.post, self.author)
