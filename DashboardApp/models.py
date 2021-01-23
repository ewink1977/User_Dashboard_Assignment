from django.db import models
from django.db.models.deletion import CASCADE

class User(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    description = models.TextField(default = 'Set Your Description!')
    user_level = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class WallPost(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(
        User,
        related_name = 'WallPost',
        on_delete = CASCADE
    )

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(
        User,
        related_name = 'CommentPost',
        on_delete = CASCADE
    )
    message = models.ForeignKey(
        WallPost,
        related_name = 'CommentPost',
        on_delete = CASCADE
    )

