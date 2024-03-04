from django.shortcuts import render, redirect
from datetime import date


def index(request):
    return render(request, 'index/index.html', {})

def today(request):
    day = date.today().strftime('%d/%m/%Y')
    return render(request, 'index/today.html', {"day": day})

# Functions

def create_new_project(request):
    return redirect('index:today')

def create_new_group(request):
    return redirect('index:today')

def create_new_list_node(request):
    return redirect('index:today')
