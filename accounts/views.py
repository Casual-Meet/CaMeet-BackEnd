import requests
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from rest_framework.generics import get_object_or_404
from accounts.serializers import UserSerializer
from .models import User
import json
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding          import force_bytes, smart_str
from .tokens     import account_activation_token
from .utils      import active_message
from django.core.exceptions         import ValidationError




#[Mypage] 학교이메일 인증
class MypageSchoolMailAuth(APIView):
    def post(self,request):
        try:
            #body =  json.loads(request.body.decode('utf-8', "ignore"))
            print("1")
            user=User.objects.get(id=request.user.id)
            print("2")
            user_id=request.user.id
            print("3")
            #email=body.get('user_auth_email')
            print("3-1")
            email=user.user_auth_email
            print(email)
            print("4")
            current_site=get_current_site(request)
            print("5")
            domain=current_site
            print("6")

            # user_id 를 url_base64 로 encode 해준다
            uidb64       = user_id
            print("7")
            # tokens.py 에서 만들었던 token 생성기로 token 생성
            token        = account_activation_token.make_token(user)
            print("8")
            # utils.py 에서 만들었던 message 를 불러온다
            message_data = active_message(domain, uidb64, token)
            print("9")

            mail_title = "이메일 인증을 완료해주세요"
            mail_to    = email
            print("10")
            email      = EmailMessage(mail_title, message_data, to=[mail_to])
            print("11")
            email.send()
            print("12")

            return JsonResponse({"message" : "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"error"   : "KEY_ERROR"}, status=400)

        except TypeError:
            return JsonResponse({"error"   : "TYPE_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"error"   : "VALIDATION_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"error"   : "NON_EXIST_USER"}, status=400)

class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid =uidb64
            print("1")
            user = User.objects.get(pk=uid)
            print("2")
            if account_activation_token.check_token(user, token):
                print("3")
                User.objects.filter(pk=uid).update(user_status=1)
                print("4")
                return redirect("http://cameet.site//accounts/mypage")
            return JsonResponse({"error": "AUTH_FAIL"}, status=400)
        except ValidationError:
            return JsonResponse({"error": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"error": "KEY_ERROR"}, status=400)


#[Mypage] 회원정보 조회,수정
class MypageUserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]    
    
    def get(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def put(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=UserSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#[Info] 회원정보 조회 
class InfoUserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]    
    
    def get(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=UserSerializer(user)
        return Response(serializer.data)


#회원이미지 수정(mypage)








#Social Login View
BASE_URL = 'http://cameet.site/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'

#state = getattr(settings, 'STATE')
state='random'

def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    print(email)
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        print("기존에 있는 유저")
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        print("post하고 왔음")
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return Response(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        print("새로가입한 유저")
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        print("post하고왔음")
        accept_status = accept.status_code
        print(accept_status)
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        print("여기까지옴")
        return Response(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    client_secret = getattr(settings, 'KAKAO_CLIENT_SECRET_KEY')
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
            headers={"Accept": "application/json"},
        )
    token_req_json = token_req.json()
    #error = token_req_json.get("error")
    #if error is not None:
    #    raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # 사용자가 이메일동의를 안할수도있어서 id값으로 이메일을 만들어서 작업함
    email = profile_json.get("kakao_account", None).get("email")
    if email is None:
        email = str(profile_json.get("id")) + "@kakao.com"
    print(profile_json, email)
    #email값이 살아있음(눈으로 확인함)
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 kakao로 가입된 유저
        print("기존에 있는 유저임")
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json,status.HTTP_200_OK)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        print("새로가입중임")
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json,status.HTTP_200_OK)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI