from django.contrib.auth.models import User
from blog.models import Post, Blog, Subscription
from .models import NewsFeed
from django.db.models import Prefetch


def get_user_subscriptions(user_id):
    """
    Получаем подписки пользователя
    """
    return Subscription.objects.filter(user_id=user_id).values_list('blog_id', flat=True)


def get_posts_for_user(user_id, limit=10):
    """
    Получаем посты для пользователя
    """
    subscriptions = get_user_subscriptions(user_id)
    posts_prefetch = Prefetch('posts',
                              queryset=Post.objects.filter(blog__id__in=subscriptions).order_by('-created_at')[:limit])
    blogs = Blog.objects.filter(id__in=subscriptions).prefetch_related(posts_prefetch)
    posts = []
    for blog in blogs:
        posts.extend(blog.posts.all())
    return posts[:limit]  # Убедитесь, что возвращаем не более limit постов


def mark_post_as_read(user_id, post_id):
    """
    Отмечаем пост как прочитанный для пользователя
    """
    NewsFeed.objects.filter(user_id=user_id, post_id=post_id).update(read=True)


def send_daily_email(user_id):
    """
    Вывести в консоль подборку из 5 последних постов ленты пользователя.
    """
    latest_posts = NewsFeed.objects.filter(user_id=user_id).order_by('-post__created_at')[:5]
    print(f"Последние 5 постов для пользователя {user_id}:")
    for news_item in latest_posts:
        post = news_item.post
        print(
            f"Заголовок: {post.title}, Текст: {post.text[:50]}...")
