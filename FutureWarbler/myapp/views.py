from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,"index.html",locals())
def login(request):
    return render(request,"login.html",locals())
def register(request):
    return render(request,"register.html",locals())
def personal(request):
    return render(request,"personal-page.html",locals())

#登入
def login(request):
    if request.method == 'POST':
        account = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=account, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/index')
            else:
                message = '帳號未啟用!'
        else:
            message = '登入失敗!'
    return render(request, "login.html", locals())
