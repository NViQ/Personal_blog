from rest_framework import serializers
from ...models import Blog, Post, Subscription


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'blog', 'title', 'text', 'created_at']


class BlogSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)


    class Meta:
        model = Blog
        fields = ['id', 'owner', 'title', 'posts']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'blog']
        