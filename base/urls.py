from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.single_room, name='room'),
    
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),

    path('delete-comment/<str:pk>/', views.delete_comment, name='delete-comment'),
    
    path('topics/', views.topics_page, name='topics'),
]




