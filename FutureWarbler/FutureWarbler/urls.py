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
from myapp.views import index,login,register,personal,classes,classcontent,indexclass,indexclasscontent,robotnormal,robotintelligent,news,news1,news2,news3,news4,news5,newscontent,newssearch,forum,forumwrite,forumcontent,trade,transactionRecord,strategy,logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index/',index),
    path('login/',login),
    path('logout/',logout),
    path('register/',register),
    path('personal/',personal),
    path('transactionRecord/',transactionRecord),
    path('class/',classes), 
    path('class-content/',classcontent),
    path('index-class/',indexclass),
    path('index-class-content/',indexclasscontent),
    path('robot-normal/',robotnormal),
    path('robot-intelligent/',robotintelligent),
    path('news/',news),
    path('news1/',news1),
    path('news2/',news2),
    path('news3/',news3),
    path('news4/',news4),
    path('news5/',news5),
    path('news-content/<int:pk>/', newscontent),
    path('news-search/',newssearch),
    path('forum/',forum),
    path('forum-write/',forumwrite),
    path('forum-content/',forumcontent),
    path('trade/',trade),
    path('strategy/',strategy),
]
