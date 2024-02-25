from django.shortcuts import render
from datetime import date


def index(request):
    return render(request, 'index/index.html', {})

def today(request):
    day = date.today().strftime('%d/%m/%Y')
    return render(request, 'index/today.html', {"day": day})
