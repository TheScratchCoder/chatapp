from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('register/', views.register, name='register'),
    path('create-room/', views.create_room, name='create_room'),
    path('room/<slug:room_slug>/', views.room_detail, name='room_detail'),
]
