from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from chikcam.users.models import User


# Create your views here.
def chicks_stream(request: HttpRequest):
    user_count = User.objects.count()
    context = {
        'user_count': user_count,
    }
    return render(request, "chicks/stream.html", context)

