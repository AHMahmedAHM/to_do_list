from django.urls import path 
from . import views 


app_name='tasks'

urlpatterns = [
    path('list/', views.tasks_list, name='tasks_list'),
    path('task_details/<slug:slug>/', views.task_details, name='task_details'),
    path('add_task/', views.add_task, name='add_task'),
    path('update_task/<slug:slug>/', views.update_task, name='update_task'),
    path('delete_task/<slug:slug>/', views.delete_task, name='delete_task'),
    path('add_category/', views.add_category, name='add_category'),
    path('change_status/<slug:slug>/', views.change_status, name='change_status')
]
