from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender='blog.Post')
def add_post_to_feeds(sender, instance, created, **kwargs):
    if created:
        NewsFeed = apps.get_model('newsfeed', 'NewsFeed')
        subscribers = instance.blog.subscribers.all()
        for subscription in subscribers:
            NewsFeed.objects.create(user=subscription.user, post=instance)

@receiver(post_delete, sender='blog.Post')
def remove_post_from_feeds(sender, instance, **kwargs):
    NewsFeed = apps.get_model('newsfeed', 'NewsFeed')
    NewsFeed.objects.filter(post=instance).delete()
