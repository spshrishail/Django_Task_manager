import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests


@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    
    request.session['user_data'] = user_data

    return redirect('sign_in')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

# List all tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'sign_in.html', {'tasks': tasks})

# View a single task
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'sign_in.html', {'task': task})

# Create a new task
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

# Edit an existing task
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

# Delete a task
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

# views.py

from django.shortcuts import render, redirect
from .models import UserInvitation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def user_register(request):
    token = request.GET.get('token')
    if not token:
        return redirect('sign_in')  # Redirect to login if no token is provided

    try:
        invitation = UserInvitation.objects.get(token=token)
    except UserInvitation.DoesNotExist:
        return redirect('sign_in')  # Redirect if the token is invalid

    if invitation.is_registered:
        return redirect('sign_in')  # If already registered, redirect to login

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            invitation.is_registered = True
            invitation.save()
            return redirect('home')  # Redirect to homepage after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})



