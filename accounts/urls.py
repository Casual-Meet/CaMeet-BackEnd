from django.contrib import admin
from django.urls import path,include
from accounts import views

urlpatterns = [
    #Mypage
    path('mypage/',views.MypageUserDetailAPIView.as_view(),name='MypageUserDetailAPIView'),
    
    #Info
    path('info/',views.InfoUserDetailAPIView.as_view(),name='InfoUserDetailAPIView'),
    
    #소셜로그인(구글)
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback,      name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    
    #소셜로그인(카카오)
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(),
         name='kakao_login_todjango'),
]