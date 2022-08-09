from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    user_profile_img=serializers.ImageField(use_url=True)
    
    
    class Meta :
        model = User #user 모델 사용
        field = '__all__' #모든 필드 포함