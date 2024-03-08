from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from datetime import date

from .models import Project, Group, ListNode
from profiles.models import Profile

def index(request):
    return render(request, 'index/index.html', {})

def today(request):
    return render(request, 'index/today.html', {"day": date.today().strftime('%d/%m/%Y')})

def project(request, slug):
    project = Project.objects.get(slug=slug)
    list_nodes = ListNode.objects.filter(project=project).order_by('-id')
    if (request.user.is_authenticated and request.user.profile.projects_allowed_in.filter(slug=slug).exists()) or request.user.profile == project.profile:
        return render(request, 'index/project.html', {"project": project, 'list_nodes': list_nodes, "created_at": project.created_at.strftime('%d/%m/%Y')})
    
    else:
        return redirect('index:today')
    
# Functions
def create_new_project(request):
    if request.user.is_authenticated:
        project = Project.objects.create(user=request.user.profile, is_today=False, title="⚡ Your New Project!")
        project.save()
    
    return redirect('index:today')

def create_new_group(request):
    return redirect('index:today')

def create_new_list_node(request):
    return redirect('index:today')

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