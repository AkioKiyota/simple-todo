from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse

from .forms import SignUpForm
from .models import Project, List, ListNode


def index(request):
    projects = Project.objects.all()

    return render(request, 'main/index.html', {'projects': projects})




def sign_in(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect('main:index')
        else:
            return render(request, 'main/sign_in.html', {'error': 'Invalid username or password.'})

    return render(request, 'main/sign_in.html')


def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return redirect('main:index')
    else:
        form = SignUpForm()

    return render(request, 'main/sign_up.html', {'form': form})

def sign_out(request):
    if not request.user.is_authenticated:
        return redirect('main:index')    
    logout(request)
    return redirect('main:sign_in')






def project_page(request, id):
    project = Project.objects.get(id=id)
    allowed_users = project.allowed_users.all()
    possible_users = User.objects.exclude(id__in=allowed_users.values_list('id', flat=True), id=project.user.id)

    project_list = project.list_set.all()
    print(project_list)

    return render(request, 'main/project_page.html', {'project': project, 'allowed_users': allowed_users})

def create_project(request):
    if request.method == 'POST':
        title = request.POST['title']
        project = Project.objects.create(title=title, user=request.user)
        return redirect('main:project_page', id=project.id)

    return render(request, 'main/create_project.html')

def delete_project(request, id):
    project = Project.objects.get(id=id)
    if request.user.is_authenticated and request.user == project.user:
        project.delete()
        return redirect('main:index')

def add_allowed_user(request):
    if request.method == 'POST':
        project = Project.objects.get(id=request.POST['project_id'])
        if request.user.is_authenticated and request.user == project.user:
            try:
                user = User.objects.get(username=request.POST['username'])
                project.allowed_users.add(user)
                return redirect('main:project_page', id=project.id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': True, 'message': 'User does not exist.'})
            except Exception as e:
                return JsonResponse({'error': True, 'message': 'An error occurred.', 'exception': str(e)})

def remove_allowed_user(request):
    if request.method == 'POST':
        project = Project.objects.get(id=request.POST['project_id'])
        if request.user.is_authenticated and request.user == project.user:
            user = User.objects.get(id=request.POST['user_id'])
            project.allowed_users.remove(user)

            return redirect('main:project_page', id=project.id)







def create_todo_list(request, project_id):
        project = Project.objects.get(id=project_id)
        if request.user.is_authenticated and (request.user in project.allowed_users.all() or request.user == project.user):
            List.objects.create(project=project, user=request.user)
            return redirect('main:project_page', id=project_id)

def create_todo_list_node(request, todo_list_id):
    todo_list = List.objects.get(id=todo_list_id)
    if request.user.is_authenticated and (request.user == todo_list.user or request.user == todo_list.project.user):
        ListNode.objects.create(list=todo_list, user=request.user)
        return redirect('main:project_page', id=todo_list.project.id)

def edit_todo_list_node(request):
    if request.method == 'POST':
        todo_list_node = ListNode.objects.get(id=request.POST['todo_list_node_id'])
        if request.user.is_authenticated and (request.user == todo_list_node.user or request.user == todo_list_node.list.project.user):
            todo_list_node.content = request.POST['content']
            todo_list_node.save()
            return HttpResponse('Success')

