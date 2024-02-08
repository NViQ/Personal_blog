from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from newsfeed.models import NewsFeed


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


@receiver(post_save, sender=Post)
def add_post_to_feeds(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.blog.subscribers.all()
        for subscription in subscribers:
            NewsFeed.objects.create(user=subscription.user, post=instance)


@receiver(post_delete, sender=Post)
def remove_post_from_feeds(sender, instance, **kwargs):
    NewsFeed.objects.filter(post=instance).delete()
