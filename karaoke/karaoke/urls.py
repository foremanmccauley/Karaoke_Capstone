"""karaoke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin

from . import views

app_name = 'karaoke'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index, name="index"),
    path('recording',views.recording, name="recording"),
    path('songselection',views.songselection, name="songselection"),
    path('register',views.register, name="register"),
    path('login',views.loginpage, name="loginpage"),
    path('logout',views.logoutuser, name="logoutuser"),
    path('profile',views.profile, name="profile"),
    path('add-friend/<int:id>/', views.send_friend_request, name='add-friend'),
    path('accept_friend/<int:id>/', views.accept_friend_request, name='accept_friend'),
    path('add-group-member/<int:id>/', views.send_group_request, name='add-group-member'),
    path('accept_group_member/<int:id>/', views.accept_group_request, name='accept_group_member'),
]
