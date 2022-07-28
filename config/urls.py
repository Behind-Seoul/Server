from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('account/login/kakao/', views.kakao_login, name='kakao_login'),
    path('account/login/kakao/callback/', views.kakao_callback, name='kakao_callback'),
]

