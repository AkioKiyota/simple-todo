from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name='index'),
    path('today/', views.today, name='today'),
    path('project/<slug:slug>/', views.project, name='project'),
    
    
    # Functions
    path('post/create_new_project/', views.create_new_project, name='create_new_project'),
    
    path('post/edit_project_name/<slug:slug>/', views.edit_project_name, name='edit_project_name'),
    path('post/add_allowed_user/<slug:slug>/', views.add_allowed_user, name='add_allowed_user'),
    path('post/remove_allowed_user/<slug:slug>/', views.remove_allowed_user, name='remove_allowed_user'),
]