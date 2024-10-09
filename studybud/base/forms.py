# Model Forms:

from django.forms import ModelForm
from .models import Rooms, User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "password1", "password2", "email"]


class RoomsForm(ModelForm):
    class Meta:
        model = Rooms
        fields = "__all__"
        exclude = ["host", "participants"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "bio", "avatar"]
