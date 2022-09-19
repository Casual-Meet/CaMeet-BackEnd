
from time import time
from django.shortcuts import render, get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.renderers import JSONRenderer

from datetime import date, timedelta


class UserList(APIView):
    
    # 역참조를 통해 user가 생성한 방을 보고싶다!
    def get(self, request):
        
        users = User.objects.all()
        # rooms = Room.objects.all()
        # print(dir(users))
        # 많은 유저 받아오려면 (many=True) 써줘야 한다! 이렇게 에러뜨는 경우가 생각보다 많다...
        serializer = UserSerializer(users, many=True)

        # renderer_classes = [JSONRenderer]
        # serializer2 = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        # db에 담기 위해 디시리얼라이즈?
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserInfo(APIView):

    def get(self, request):

        user = request.user
        serializer = UserSerializer(user)
    
        return Response(serializer.data)


class RoomList(APIView):

    def get(self, request):

        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)

# 일주일치 room정부 불러옴
class AWeekRoomList(APIView):

    def get(self, request):
        
        room = Room.objects.filter(room_date__range=[date.today(), date.today()+timedelta(days=7)]).all()
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)

class RoomDetailAPIView(APIView):
    
    def get_object(self, pk):
        room = get_object_or_404(Room, pk=pk)
        # room_info = room.user__id
        return room
    
    def get(self, request, pk):
        # 특정 pk값에 해당하는 room 객체 가져옴.
        room = self.get_object(pk)
        serializer = RoomSerializer(room)
        print(serializer)
        return Response(serializer.data)

    def post(self, request, pk):
        id = request.user.id
        host=User.objects.get(id=id)
        room=Room.objects.get(id=pk)
        apply_counter = Apply.objects.filter(room_id_id = pk)
        
        try:
            #방생성자가 신청을 한다면? 호스트는 참가하기를 누를 수 없습니다.
            if room.user_key==host.email:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            #이미 신청을 한 유저라면? 이미 신청을 한 유저입니다.
            obj=Apply.objects.filter(room_id_id=pk)&Apply.objects.filter(user_id_id=id)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Apply.DoesNotExist:
            serializer = RoomApplySerializer(data = request.data)
            roomHeadcount = Room.objects.get(id = pk).room_headcount
            if serializer.is_valid():
                serializer.save()
        
            if len(apply_counter) == roomHeadcount:
                room = Room.objects.get(id = pk)
                room.room_status = 2
                room.save()
            return Response(serializer.data)

class RoomCreateAPIView(APIView):
    
    def post(self, request):
        id=request.user.id
        request.data['user_key']=id
        serializer = RoomcreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)