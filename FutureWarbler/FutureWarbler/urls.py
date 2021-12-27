"""FutureWarbler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myapp.views import index,login,register,personal,classes,classcontent,news,newscontent,forum,forumwrite,forumcontent,trade,transactionRecord,strategy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index/',index),
    path('login/',login),
    path('register/',register),
    path('personal/',personal),
    path('transactionRecord/',transactionRecord),
    path('class/',classes), #change
    path('class-content/',classcontent),
    path('news/',news),
    path('news-content',newscontent),
    path('forum/',forum),
    path('forum-write/',forumwrite),
    path('forum-content/',forumcontent),
    path('trade/',trade),
    path('strategy/',strategy),
]
