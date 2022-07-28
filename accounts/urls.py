from django.urls import path
from accounts import views

urlpatterns = [
    path('kakao/login/finish/', views.KakaoLogin.as_view(),
         name='kakao_login_todjango'),
]