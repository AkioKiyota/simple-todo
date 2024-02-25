from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),

    path('project/<int:id>/', views.project_page, name='project_page'),
    path('create_project/', views.create_project, name='create_project'),
    path('delete_project/<int:id>/', views.delete_project, name='delete_project'),

    path('create_todo_list/<int:project_id>/', views.create_todo_list, name='create_todo_list'),
    path('create_todo_list_node/<int:todo_list_id>/', views.create_todo_list_node, name='create_todo_list_node'),
    path('edit_todo_list_node/', views.edit_todo_list_node, name='edit_todo_list_node'),

    path('add_allowed_user/', views.add_allowed_user, name='add_allowed_user'),
    path('remove_allowed_user/', views.remove_allowed_user, name='remove_allowed_user'),

]
