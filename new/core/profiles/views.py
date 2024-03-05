from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse

from .forms import SignUpForm
from .models import Profile
from index.models import Project, Group, ListNode

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect('index:index')
        else:
            return render(request, 'profiles/sign_in.html', {'error': 'Invalid username or password.'})

    return render(request, 'profiles/sign_in.html')


def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            today_project = Project.objects.create(user=profile, is_today=True, title="Today")
            
            login(request=request, user=user)
            return redirect('index:index')
    else:
        form = SignUpForm()

    return render(request, 'profiles/sign_up.html', {'form': form})

def sign_out(request):
    if not request.user.is_authenticated:
        return redirect('profiles:index')    
    logout(request)
    return redirect('profiles:sign_in')
