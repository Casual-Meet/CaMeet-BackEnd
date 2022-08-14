from dataclasses import field, fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    # (시행착오)
    # 유저가 생성한 방들 가져오기 위해 역참조

    # 역참조 ; 여기 변수는 FK부분 related_name 이랑 같아야함.
    # rooms = RoomSerializer(many=True, read_only=True)
    # rooms = serializers.StringRelatedField(many=True)


    # SerializerMethodField() 의 속성으로 method_name='' 을 줄 수 있다.
    # 없다면 함수명은 get_(변수명)이어야 올바르게 작동한다.
    user_create_rooms = serializers.SerializerMethodField()
    user_join_rooms = serializers.SerializerMethodField()
    class Meta:
        model = User
        # fields = '__all__'      # 필요한 필드만 하고 싶을 땐 리스트 형태로 작성. ; fields = ['id', 'title']

        # User객체에 없는, room정보도 SerializerMethodField()로 가져온 변수도 넣어주기!
        # SerializerMethodField()로 추가한 변수명도 필드에 추가해줘야함!
        fields = ('email', 'user_create_rooms', 'user_join_rooms')
        # 읽기만 할 수 있는 것들 ; 이걸 명시해주면 읽기만 하니까 속도가 더 빠른 듯.
        #read_only_fields = ('name', 'age','created')

    # get_(변수명)이어야 올바르게 작동한다.
    def get_user_create_rooms(self, obj):

        room_list = []

        # 받아온 객체가 쿼리셋 형태라 json 형태로 풀어주기위해 (안해주면 시리얼라이즈 안됏다고 오류뜸...)
        for room in obj.rooms.all():
            # print(obj)
            room_json = {
                'room_id': room.id,
                'room_title' : room.room_title,
                'room_interest' : room.room_interest,
            }

            room_list.append(room_json)

        # 문제) 지금 room_list 는 json으로 시리얼라이즈 되지 않았다,,, ->객체들을 json 형태로 하나씩 담아주는 방법 선택

        return room_list

    def get_user_join_rooms(self, obj):

        apply_list = []

        # 받아온 user객체를 join이라는 related_name으로 역참조해서 apply 객체로 연결
        for apply in obj.join.all():

            # apply객체롤 통해 룸정보에 접근하기 위해 room_id로 room 객체에 가서 각각의 룸정보 뽑아옴.
            apply_json = {
                'room_id': apply.room_id.id,
                'room_title': apply.room_id.room_title,
                'room_interest': apply.room_id.room_interest,
            }
            apply_list.append(apply_json)

        return apply_list



# 룸정보 안에 유저정보까지
class RoomSerializer(serializers.ModelSerializer):

    host = serializers.SerializerMethodField()

    # user_id = serializers.StringRelatedField()
    
    # 중요) 변수명을 모델에서 쓴 변수명으로 통일해줘야 함.(FK필드)
    # 참고로 방의 호스트(user)는 한명이니 many=True 써주면 안된다.

    # userserializer를 쓰면 시리얼라이저 안에 담긴 투머치한 정보까지 줘서 문제,,,
    # user_key = UserSerializer()
    # user_key = UserSerializer(read_only = True)    

    class Meta:
        model = Room
        # fields = [ 'room_title', 'user']
        fields = ('id', 'room_title', 'room_interest', 'room_place','room_date','room_time','room_headcount','room_status','room_created_time','host')
        # fields = ['id', 'user_key', 'room_title', 'room_interest']
        # unique_together = ['user_id', 'room_title']
    
    def get_host(self, obj):

        # 호스트는 객체가 하나라 for문이 아니라 그냥 json 형태로 담아주기만 하면 됨.
        user_json = {
                #'user_id': obj.user_key.name,
                'email' : obj.user_key.email,
                #'user_age' : obj.user_key.created,
            }
        return user_json

# 이건 안씀.
class ApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Apply
        fields = '__all__'

class RoomcreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

class RoomApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Apply
        fields = '__all__'