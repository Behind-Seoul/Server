from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin


from .models import User

BASE_URL = "http://34.64.220.170:8000/"
KAKAO_CALLBACK_URI = BASE_URL + "account/login/kakao/callback/"

state = getattr(settings, "STATE")

def kakao_login(request):
    rest_api_key = getattr(settings, "KAKAO_REST_API_KEY")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


@api_view(['GET'])
def kakao_callback(request):
    CODE = request.GET['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
            'grant_type': 'authorization_code',
            'client_id': getattr(settings, "KAKAO_REST_API_KEY"),
            'redirect_url': KAKAO_CALLBACK_URI,
            'code': CODE
        }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    # 그 이후 부분
    tokenJson = response.json()
    userUrl = "https://kapi.kakao.com/v2/user/me" # 유저 정보 조회하는 uri
    auth = "Bearer "+tokenJson['access_token'] ## 'Bearer '여기에서 띄어쓰기 필수!!
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(userUrl, headers=HEADER)
    return Response(res.text)



class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
