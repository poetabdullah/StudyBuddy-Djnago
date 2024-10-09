"""
URL configuration for studybud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

""" The things get pretty messy if we deal with it here.
So, we can write these in views.py
def home(request):  # What's being sent to the backend
    return HttpResponse("Home Page")


def rooms(request):
    return HttpResponse("Rooms")

"""


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),  # Include the app-level URLs
    path("api/", include("base.api.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
