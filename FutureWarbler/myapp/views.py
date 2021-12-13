from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html",locals())
def login(request):
    return render(request,"login.html",locals())
def register(request):
    return render(request,"register.html",locals())
def personal(request):
    return render(request,"personal-page.html",locals())