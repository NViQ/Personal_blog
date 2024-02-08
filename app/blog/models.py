from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.blog.title}"
