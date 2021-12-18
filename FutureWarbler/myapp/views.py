from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import time
import pymysql


#連線至資料庫
db_settings = {
"host": "localhost",
"port": 3306,
"user": "root",
"password": "12345678",
"db": "futurewarbler",
"charset": "utf8"
}
conn = pymysql.connect(**db_settings)

# Create your views here.
def index(request):
    return render(request,"index.html",locals())

#--------------登入功能------------------

def login(request):
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        if account == "" or password =="":
             message = '登入失敗!請確認帳號或者密碼是否正確'
        else:
            with conn.cursor() as cursor:
                sql = "SELECT `member_password` FROM `member` WHERE member_id='%s'"%(account)
                cursor.execute(sql)
                data = cursor.fetchone()
                if password == data[0]:
                    request.session['username'] = account
                    return redirect('/index')
                else:
                    message = '登入失敗!請確認帳號或者密碼是否正確'
            conn.close()
    return render(request,"login.html",locals())

#--------------註冊功能------------------
def register(request):
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        photopath = request.FILES.get('photo',False)
        name = request.POST['name']
        gender = request.POST['gender']
        birth = request.POST['birth']
        phone = request.POST['phone']
        mail = request.POST['mail']
        if account== "" or password == ""  or name== "" or photopath==False or gender =="" or birth == "" or phone =="" or mail=="":
            lostSomething ="lostSomething"
            checkLost= "您少填了部分資料請先再次檢查"
            return render(request,"register.html",locals())
        else:
            if gender == 0:
                sex = 'M'
            else:
                sex = 'F' 
            with conn.cursor() as cursor:
                sql = "SELECT * FROM `member` WHERE `member_id` LIKE ('%s')"%(account)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    check = 'no'
                    message = '您輸入的帳戶有人使用，請重新輸入帳戶:'
                    return render(request,"register.html",locals())
                else:
                    #照片上傳部分
                    photo = request.FILES['photo']
                    photoname = request.FILES['photo'].name
                    uploadphoto  = account+'_'+photoname
                    with open('static/userimg/'+uploadphoto, 'wb+') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                    #-----------
                    sql = "INSERT INTO `member`(`member_id`, `member_password`, `member_name`, `member_photo`, `member_gender`, `member_birth`, `member_phone`, `member_email`) VALUES ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s')"%(account, password, name, uploadphoto, sex, birth, phone, mail)
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                    request.session['username'] = account
                    return render(request,'index.html',locals())
            
    return render(request,"register.html",locals())


def personal(request):
    return render(request,"personal-page.html",locals())

def logout(request):
    request.session.clear()
    return redirect('login/')




