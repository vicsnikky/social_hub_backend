from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    media = models.FileField(upload_to="post_media/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:30]}"


class Like(models.Model):
    """
    Explicit join model for likes. Keep this model and do NOT also add a
    liked_by = ManyToManyField(...) on Post at the same time to avoid migration conflicts.
    Use this model in views/serializers to list likes:
        Like.objects.filter(post=post)  or post.like_set.all()
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # no related_name — reverse is post.like_set
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Keep comment likes as a ManyToMany - these are independent from the Post.like model
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_comments",
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} commented on Post {self.post.id}"
