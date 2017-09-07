# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# local Django
from .forms import EventForm
from .models import Event
from accounts.backends import UserBackend
from accounts.models import User


def list_events(request):
    """
    This function is used for creating a view that lists out all of the events
    in an organized manner.

    :type request: django.http.request.HttpRequest
    :param request: Request object that contains information from the user's POST/GET request.

    :rtype: django.shortcuts.render
    :returns: An HTML rendered page of 'listEvents.html' that has all of the
             Event objects passed into it.
    """
    return render(request, 'events/listEvents.html', {'eventsList': Event.objects.all()})


def create_event(request):
    """
    This view allows authenticated users to create events.

    :type request: django.http.request.HttpRequest
    :param request: Request object that contains information from the user's POST/GET request.

    :rtype: django.shortcuts.render or django.http.HttpResponseRedirect
    :returns:

    - If the user is not a superuser, they will be redirected to a 404 error page.
    - If the user is a superuser:
        - If the user is submitting a GET request, it will send them to the blank create
          event page.
        - If the user is submitting a POST request:
            - If the form is valid, it will save the event to the database and redirect the user
              to the homepage.
            - If the form is invalid, the user will be redirected back to the same create event
              page with same information that they filled out, but also with information that now
              explains the errors that occured when they tried to submit their event.
    """

    # Used for testing purposes
    #request.user = UserBackend().authenticate('zdw27f@mst.edu')

    # Temporary (until permissions are setup): makes sure the user attempting
    # to create an event is a superuser.
    if not request.user.is_superuser:
        return render(request, '404.html')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        # Validates form and adds creator to event
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return HttpResponseRedirect("/")

        return render(request, 'events/create-event.html', {'form': form})

    # Sends user to create event page if the user has permission to do so
    return render(request, 'events/create-event.html', {'form': EventForm})
