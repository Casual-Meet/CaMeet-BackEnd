
from django.contrib import admin
from django.urls import path
from room import views

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('room/', views.RoomList.as_view()),
    path('room/<int:pk>', views.RoomDetailAPIView.as_view()),

    path('info/', views.UserInfo.as_view()),

]