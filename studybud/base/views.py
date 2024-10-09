# base/views.py
from django.shortcuts import render, redirect
from .models import Rooms, Topic, Message, User
from .forms import RoomsForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# List of rooms
"""
rooms_view = [
    {"id": 1, "name": "Lets learn Python"},
    {"id": 2, "name": "Design with me"},
    {"id": 3, "name": "Frontend Developers"},
]
"""


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, "The user does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    # page = "register"
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, "base/login_register.html", {"form": form})


# Home view that renders the rooms list on the homepage
def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms_view = Rooms.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms_view.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms_view,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


# Room view that renders details of a specific room based on pk
def room_view(request, pk):
    room = Rooms.objects.get(id=pk)
    room_messages = room.message_set.all()

    # Fetch participants associated with the room
    participants = (
        room.participants.all()
    )  # Assuming `participants` is a related name in your model

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)  # Use 'room', not 'room_view'

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,  # Include participants here
    }
    return render(request, "base/rooms.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomsForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Rooms.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        # form = RoomsForm(request.POST)
        # if form.is_valid():
        #     rooms = form.save(commit=False)
        #     rooms.host = request.user
        #     rooms.save()
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    rooms = Rooms.objects.get(id=pk)
    form = RoomsForm(instance=rooms)
    topics = Topic.objects.all()

    if request.user != rooms.host:
        return HttpResponse("You do not enough permissions to carry this request.")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        rooms.name = request.POST.get("name").POST.get("name")
        rooms.topic = request.POST.get("topic")
        rooms.description = request.POST.get("description")
        rooms.save()
        # form = RoomsForm(request.POST, instance=rooms)
        # if form.is_valid():
        # form.save()
        return redirect("home")
    context = {"form": form, "topics": topics, "rooms": rooms}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    rooms = Rooms.objects.get(id=pk)
    if request.user != rooms.host:
        return HttpResponse("You do not enough permissions to carry this request.")
    if request.method == "POST":
        rooms.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": rooms})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You do not enough permissions to carry this request.")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {"form": form})


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {"topics": topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})
