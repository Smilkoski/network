from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    def serializable(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email}


class Follower(models.Model):
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ufs')
    following_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ufg')


class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def serialize(self):
        date = f'{self.date_posted.day} {self.date_posted.strftime("%B")}, {self.date_posted.year}'
        return {
            "id": self.id,
            "content": self.content,
            "date_posted": date,
            "author": self.author.serializable()
        }


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_id')

    def serialize(self):
        return {
            'user': self.user.id,
            'liked_post': self.liked_post.id,
        }
