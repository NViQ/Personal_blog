from django.db import models
from django.contrib.auth.models import User
from blog.models import Post


class NewsFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')
