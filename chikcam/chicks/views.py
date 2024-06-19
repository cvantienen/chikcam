from django.http import HttpRequest
from django.shortcuts import render
from django.contrib import messages
from chikcam.users.models import User


# Create your views here.
def chicks_stream(request: HttpRequest):
    # Clear messages after they have been displayed
    storage = messages.get_messages(request)
    for message in storage:
        pass  # This will mark the message as read

    # Get the number of users in the database
    user_count = User.objects.count()
    context = {
        'user_count': user_count,
    }
    return render(request, "chicks/stream.html", context)

