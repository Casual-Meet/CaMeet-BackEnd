from django.contrib import admin
from django.urls import path
from room import views

urlpatterns = [
    # 유저정보 전체 리스트업하는 url
    path('userlist/', views.UserList.as_view()),
    # 로그인한 유저정보 불러오는 url -> 햄버거info 창에서 사용
    path('userinfo/', views.UserInfo.as_view()),
    # room정보 전체 리스트업하는 url
    path('roomlist/', views.RoomList.as_view()),
    # 일주일치 room정보 전체 리스트업하는 url
    path('aweek-roomlist/', views.AWeekRoomList.as_view()),
    # 특정 room 정보 불러오는 url
    path('roomdetail/<int:pk>', views.RoomDetailAPIView.as_view()),
    # 방생성 post 요청보내는 url
    path('roomcreate/', views.RoomCreateAPIView.as_view())
]