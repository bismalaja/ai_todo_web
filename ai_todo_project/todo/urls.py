from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_todo, name='add_todo'),
    path('delete/<uuid:todo_id>/', views.delete_todo, name='delete_todo'),
    path('complete/<uuid:todo_id>/', views.complete_todo, name='complete_todo'),
    
    # Add authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]