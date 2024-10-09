from django.contrib import admin
from .models import Rooms, Topic, Message

# Register your models here.
admin.site.register(Rooms)
admin.site.register(Topic)
admin.site.register(Message)
