from django.contrib import admin
from django.urls import path
from room import views

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('list/', views.RoomList.as_view()),
    path('detail/<int:pk>', views.RoomDetailAPIView.as_view()),
    path('create/', views.RoomCreateAPIView.as_view())

]