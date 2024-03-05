from django.shortcuts import render, redirect
from datetime import date

from .models import Project, Group, ListNode

def index(request):
    return render(request, 'index/index.html', {})

def today(request):
    day = date.today().strftime('%d/%m/%Y')
    return render(request, 'index/today.html', {"day": day})

def project(request, slug):
    if request.user.is_authenticated and request.user.profile.projects_allowed_in.filter(slug=slug).exists():
        project = Project.objects.get(slug=slug)
        return render(request, 'index/project.html', {"project": project})
    
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
