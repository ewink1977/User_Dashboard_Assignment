from django.db import models
from django.db.models.deletion import CASCADE
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['register-email']):
            errors['invalid-email'] = 'Your email is invalid. Please try again.'
        email_check = User.objects.filter(email = postData['register-email'])
        if email_check == postData['register-email']:
            errors['email'] = 'Email already exists. Please log in or use another email.'
        if not postData['register-password'] == postData['register-confirm-pw']:
            errors['confirmpassword'] = 'Password mismatch! Please try again!'
        if len(postData['register-password']) < 8:
            errors['password'] = 'Your password must be at least 8 characters long.'
        return errors

class User(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    description = models.TextField(default = 'Set Your Description!')
    user_level = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

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

