from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import User

from django.db.models.deletion import CASCADE


class User(AbstractUser):
    name = models.CharField(
        max_length=200, null=True, blank=True
    )  # Allow blank names in forms
    email = models.EmailField(
        null=True, blank=True, unique=True
    )  # Consider adding blank=True
    bio = models.TextField(null=True, blank=True)  # Allow empty bio
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # One to Many relationship
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]
