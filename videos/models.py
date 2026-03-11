from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Video(models.Model):
    # Use UUIDField instead of CharField for unique IDs
    video_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    views = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(default=timezone.now)
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-upload_date"]

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.likes.filter(is_like=True).count()

    def get_dislikes_count(self):
        return self.likes.filter(is_like=False).count()

    def increment_views(self):
        self.views += 1
        self.save(update_fields=["views"])


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)  # True = like, False = dislike
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("video", "user")

    def __str__(self):
        action = "liked" if self.is_like else "disliked"
        return f"{self.user.username} {action} {self.video.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name="subscriptions", blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    def get_subscriber_count(self):
        return self.subscribers.count()
