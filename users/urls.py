from django.urls import path

from . import views

urlpatterns = [
    path('profile/<str:pk>/', views.user_profile, name='profile'),
    path('profile-edit/<str:pk>/', views.user_profile_edit, name='profile-edit'),

    path('login/', views.user_login, name='login'),
    path('registration/', views.user_registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    
    path('activity/', views.activity_page, name='activity'),

]