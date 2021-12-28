from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    pass


class Follower(models.Model):
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ufs')
    following_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ufg')


class Post(models.Model):
    title = models.CharField(max_length=240)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
