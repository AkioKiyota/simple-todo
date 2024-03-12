from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from datetime import date
from itertools import chain

from .models import Project, Group, ListNode
from profiles.models import Profile

def index(request):
    return render(request, 'index/index.html', {})

def today(request):
    return render(request, 'index/today.html', {"day": date.today().strftime('%d/%m/%Y')})

def project(request, slug):
    project = Project.objects.get(slug=slug)
    list_nodes = ListNode.objects.filter(project=project).all()
    groups = Group.objects.filter(project=project).all()
    
    objects = sorted(
        chain(list_nodes, groups),
        key=lambda object: object.created_at,
        reverse=True
    )
    

    if (request.user.is_authenticated and request.user.profile.projects_allowed_in.filter(slug=slug).exists()) or request.user.profile == project.profile:
        return render(request, 'index/project.html', {"project": project, 'groups': groups, 'objects': objects, "created_at": project.created_at.strftime('%d/%m/%Y')})
    
    else:
        return redirect('index:today')
    
# Functions
def create_new_project(request):
    if request.user.is_authenticated:
        project = Project.objects.create(profile=request.user.profile, is_today=False, title="⚡ Your New Project!")
        slug = project.slug
        project.save()
    
    return redirect('index:project', slug=slug)

def edit_project_name(request, slug):
    project = Project.objects.get(slug=slug)
    if request.method == 'POST' and (request.user.profile.projects_allowed_in.filter(slug=slug).exists() or request.user.profile == project.profile):
        project.title = request.POST['title']
        project.save()
        return redirect('index:project', slug=slug)
    else:
        return HttpResponse("You are not allowed to access this page.")

def add_allowed_user(request, slug):
    project = Project.objects.get(slug=slug)
    if request.method == 'POST' and request.user.profile == project.profile:
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            project.allowed_users.add(User.objects.get(username=username).profile)
            project.save()
            return JsonResponse({"status": "success", "message": "User added."})
        else:
            return JsonResponse({"status": "error", "message": "User not found."})
    else:
        return JsonResponse({"status": "error", "message": "You are not allowed to do that!"})

def remove_allowed_user(request, slug):
    project = Project.objects.get(slug=slug)
    if request.method == 'POST' and request.user.profile == project.profile:
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            project.allowed_users.remove(User.objects.get(username=username).profile)
            project.save()
            return JsonResponse({"status": "success", "message": "User removed."})
        else:
            return JsonResponse({"status": "error", "message": "User not found."})
    else:
        return JsonResponse({"status": "error", "message": "You are not allowed to do that!"})