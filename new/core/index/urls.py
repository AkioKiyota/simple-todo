from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name='index'),
    path('today/', views.today, name='today'),
    
    # Functions
    path('create_new_project', views.create_new_project, name='create_new_project'),
    path('create_new_group', views.create_new_group, name='create_new_group'),
    path('create_new_list_node', views.create_new_list_node, name='create_new_list_node'),
]