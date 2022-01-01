from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import time
import pymysql
from django.core.paginator import Paginator, Page  # 翻頁
from django.db import connection, connections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import math
import pymysql.cursors
from myapp.models import News,Class as study,IndexClass
from pymysql import cursors
from django.db import connection
#連線至資料庫
db_settings = {
"host": "localhost", 
"port": 3306,
"user": "root",
"password": "12345678", 
"db": "futurewarbler",
"charset": "utf8",
"cursorclass": pymysql.cursors.DictCursor
}
conn = pymysql.connect(**db_settings)

# Create your views here.
def index(request):
    
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
    return render(request,"index.html",locals())

#---------------登出----------------------
def logout(request):
    if request.method == 'POST': 
        if request.POST['logout'] =="logout":
            request.session.flush()
    return redirect('/index/')    

#--------------登入功能------------------

def login(request):
    if 'username' in request.session:
        return  redirect('/index/') #如果處於登入狀態，只要人為方式回到login，就會自動跳轉到index
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        cursor = connection.cursor()

        sql = "SELECT * FROM `member` WHERE `member_id` ='%s'"%(account)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data == None: #這個帳號沒人註冊
            message = '此帳號尚未註冊，請再次確認'
        else:
            if password != data[1]: #帳號密碼錯誤
                message ='帳號密碼錯誤，請再次確認'
            else:
                request.session['userid'] = account
                request.session['username'] = data[2]
                request.session['gender'] = data[3]
                request.session['birth'] = data[4].strftime("%Y-%m-%d") #type=datetime.date
                request.session['photo'] = data[5]
                request.session['phone'] = data[6]
                request.session['mail'] = data[7]
                
                return redirect('/index/') 
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
                    request.session['photo'] = uploadphoto
                    photo = request.session['photo']
                    username = request.session['username']
                    return render(request,'index.html',locals())
            
    return render(request,"register.html",locals())


#------------未登入狀態下的個人頁面-----------------
def personal_unlogin(request):
    if 'username' in request.session:
         return  redirect('/personal/')
    return render(request,"personal-page(unlogin).html",locals())

#------------登入狀態下的個人頁面-----------------
def personal(request):
          
    if 'username' in request.session:
        ok = "yes"
        username = request.session['username']
        photo = request.session['photo']
        userid = request.session['userid']
        gender = request.session['gender']
        if gender =='F':
            gender = '女'
        else:
            gender = '男'
        phone = request.session['phone']
        mail = request.session['mail']
        birth = request.session['birth']
    else:
       return redirect('/personal-unlogin/')
    
    return render(request,"personal-page.html",locals())




# ------------個人介面交易紀錄-----------------------
def transactionRecord (request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        return redirect ('/personal-unlogin/')
    return render(request,"personal-transactionRecord.html",locals())


# ------------個人介面策略清單-----------------------
def strategy (request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        return redirect ('/personal-unlogin/')
    return render(request,"personal-strategyList.html",locals())

#-------模擬交易所---------------------
def trade (request):
    return render(request,"trade.html",locals())


#------------期貨小教室---------------------------------
def classes(request):          
    # if 'keyWord' in request.GET:
    #     keyWord = request.GET['keyWord']
    #     keyWord2 = '期貨'
    #     results = study.objects.filter(class_title__contains=keyWord2)
    #     import urllib.parse
    #     urllib.parse.unquote(results)
    #     print(keyWord)
    #     print(results)
    #     for i in results:
    #         print(i)
    #     return render(request, "class.html", {'results': results})
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username= 'no'
        photo ='no'
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])*6
            results = study.objects.all()[page-6:page] # Class as study  # [page-6:page]代表一頁資料數量
            return render(request, "class.html", {'results': results, 'ok': ok, 'username' : username,'photo': photo} )
        except:
            results = study.objects.all()[:6]
            return render(request, "class.html", {'results': results, 'ok': ok, 'username' : username,'photo': photo})
    else:
        results = study.objects.all()[:6]
        return render(request, "class.html",{'results': results, 'ok': ok, 'username' : username,'photo': photo})     


    # results = {}
    # sql = "SELECT `class_id`,`class_title`,`class_article`,`class_photo` FROM `class`"
    # with conn.cursor() as cursor:
    #     cursor.execute(sql)
    #     results['articles'] = cursor.fetchall() 

    # cursor23 = conn.cursor()
    # cursor23.execute("SELECT `class_id`,`class_title`,`class_article`,`class_photo` FROM `class`")
    # articles = cursor23.fetchall()
    # return render(request,"class.html", articles)

def SelectKeyWord(request):
    if 'keyWord' in request.GET:
        keyWord = request.GET['keyWord']
        news2 = News.objects.filter(news_title__iexact=keyWord)
    return render(request, "news-1.html", {'News2': news2, 'News3': news3})

def classcontent(request, pk):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username= 'no'
        photo ='no'
    cursor = conn.cursor()
    cursor.execute("select class_id,class_title,class_article,class_photo from class where class_id=%s" % (pk))
    class1 = study.objects.filter(pk=pk)
    class1 = cursor.fetchall()
    return render(request,"class-content.html", {'Class1': class1, 'ok': ok, 'username' : username,'photo': photo})

def indexclass(request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username= 'no'
        photo ='no'
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])*6
            results = IndexClass.objects.all()[page-6:page] # [page-6:page]代表一頁資料數量
            return render(request, "index-class.html",  {'results': results ,'ok': ok, 'username' : username,'photo': photo })
        except:
            results = IndexClass.objects.all()[:6]
            return render(request, "index-class.html", {'results': results, 'ok': ok, 'username' : username,'photo': photo })
    else:
        results = IndexClass.objects.all()[:6]
        return render(request, "index-class.html", {'results': results, 'ok': ok, 'username' : username,'photo': photo })

    # results = {}
    # sql = "SELECT `index_class_id`,`index_class_title`,`index_class_article`,`index_class_photo` FROM `index_class`"
    # with conn.cursor() as cursor:
    #     cursor.execute(sql)
    #     results['articles'] = cursor.fetchall()
    # return render(request,"index-class.html",results)

def indexclasscontent(request,pk):
    cursor = conn.cursor()
    cursor.execute("select index_class_id,index_class_title,index_class_article,index_class_photo from index_class where index_class_id=%s" % (pk))
    indexclass1 = IndexClass.objects.filter(pk=pk)
    indexclass1 = cursor.fetchall()
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username= 'no'
        photo ='no'
    return render(request,"index-class-content.html",{'Indexclass1': indexclass1 ,'ok': ok, 'username' : username,'photo': photo})

def robotnormal(request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
    return render(request,"robot-normal.html",locals())

def robotintelligent(request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
    return render(request,"robot-intelligent.html",locals())



def news(request):
#new2 最新 news3熱門
#如果html 裡 category=category ，判斷是category 0 財經 1 期貨 2 兩岸 3  國際 4產業 5理財
#news3裡 抓category 裡的type最新與熱門
#如果try 裡抓page一頁有幾個，下一頁
#except 防止報錯
#else 防止報錯
# print(request.GET['page'])
    if 'category' in request.GET:
        category = int(request.GET['category'])
        news3=News.objects.filter(news_category=category).filter(news_type=1)[:4]
        titleWord = {
            "0":"財經",
            "1":"期貨",
            "2":"兩岸",
            "3":"國際",
            "4":"產業",
            "5":"理財"
        }
        title = titleWord[str(category)]
        if 'page' in request.GET:
            try:   
                page = int(request.GET['page'])*5
                news2 = News.objects.all()[page-4:page]
                return render(request, "news-1.html", {'News2': news2, 'News3': news3,"title":title,"category":str(category)})
            except:
                page = request.GET['page']
                news2 = News.objects.all()[:5]
                return render(request, "news-1.html", {'News2': news2, 'News3': news3,"title":title,"category":str(category)})
        else:
            category = int(request.GET['category'])
            news2 = News.objects.filter(news_category=category).filter(news_type=0)[:5]
            news3=News.objects.filter(news_category=category).filter(news_type=1)[:5]
            return render(request, "news-1.html", {'News2': news2, 'News3': news3,"title":title})
    else:

        news3 = News.objects.all()[:5]
        news2 = News.objects.all()[:5]
        return render(request, "news-1.html", {'News2': news2, 'News3': news3})




def newscontent(request, pk):
    cursor0 = connection.cursor()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    cursor4 = connection.cursor()
    cursor5 = connection.cursor()
    cursor6 = connection.cursor()
    cursor7 = connection.cursor()
    cursor8 = connection.cursor()
    cursor9 = connection.cursor()
    cursor10 = connection.cursor()
    cursor11 = connection.cursor()
    cursor12 = connection.cursor()
    cursor13 = connection.cursor()
    cursor14 = connection.cursor()
    cursor15 = connection.cursor()
    cursor16 = connection.cursor()
    cursor17 = connection.cursor()
    cursor18 = connection.cursor()
    cursor19 = connection.cursor()
    cursor20 = connection.cursor()
    cursor21 = connection.cursor()
    cursor22 = connection.cursor()

    cursor0.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['0'])
    cursor1.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['1'])
    cursor2.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['2'])
    cursor3.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['3'])
    cursor4.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['4'])
    cursor5.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['5'])
    cursor6.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['6'])
    cursor7.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['7'])
    cursor8.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['8'])
    cursor9.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['9'])
    cursor10.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['10'])
    cursor11.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['11'])
    cursor12.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor13.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor14.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor15.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor16.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor17.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor18.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor19.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor20.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor21.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor22.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))

    news1 = News.objects.filter(pk=pk)
    news2 = News.objects.filter(pk=pk)
    news3 = News.objects.filter(pk=pk)
    news4 = News.objects.filter(pk=pk)
    news5 = News.objects.filter(pk=pk)
    news6 = News.objects.filter(pk=pk)
    news7 = News.objects.filter(pk=pk)
    news8 = News.objects.filter(pk=pk)
    news9 = News.objects.filter(pk=pk)
    news10 = News.objects.filter(pk=pk)
    news11 = News.objects.filter(pk=pk)
    news12 = News.objects.filter(pk=pk)
    news13 = News.objects.filter(pk=pk)
    news14 = News.objects.filter(pk=pk)
    news15 = News.objects.filter(pk=pk)
    news16 = News.objects.filter(pk=pk)
    news17 = News.objects.filter(pk=pk)
    news18 = News.objects.filter(pk=pk)
    news19 = News.objects.filter(pk=pk)
    news20 = News.objects.filter(pk=pk)
    news21 = News.objects.filter(pk=pk)

    news0 = cursor0.fetchall()[:5]
    news1 = cursor1.fetchall()[:5]
    news2 = cursor2.fetchall()[:5]
    news3 = cursor3.fetchall()[:5]
    news4 = cursor4.fetchall()[:5]
    news5 = cursor5.fetchall()[:5]
    news6 = cursor6.fetchall()[:5]
    news7 = cursor7.fetchall()[:5]
    news8 = cursor8.fetchall()[:5]
    news9 = cursor9.fetchall()[:5]
    news10 = cursor10.fetchall()
    news11 = cursor11.fetchall()
    news12 = cursor12.fetchall()
    news13 = cursor13.fetchall()
    news14 = cursor14.fetchall()
    news15 = cursor15.fetchall()
    news16 = cursor16.fetchall()
    news17 = cursor17.fetchall()
    news18 = cursor18.fetchall()
    news19 = cursor19.fetchall()
    news20 = cursor20.fetchall()
    news21 = cursor21.fetchall()

    return render(request, "news-content.html", {'News0': news0, 'News1': news1,'News2': news2, 'News3': news3, 'News4': news4, 'News5': news5, 'News6': news6, 'News7': news7, 'News8': news8, 'News9': news9, 'News10': news10, 'News11': news11, 'News12': news12, 'News13': news13, 'News14': news14, 'News15': news15, 'News16': news16, 'News17': news17, 'News18': news18, 'News19': news19, 'News20': news20, 'News21': news21})


def news1(request):
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    cursor2.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['2'])
    cursor3.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['3'])
    news2 = cursor2.fetchall()[:5]
    news3 = cursor3.fetchall()[:5]
    # 期貨
    return render(request, "news-1.html", {'News2': news2, 'News3': news3})
    
def news2(request):
    cursor4 = connection.cursor()
    cursor5 = connection.cursor()
    cursor4.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['4'])
    cursor5.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['5'])
    news4 = cursor4.fetchall()[:5]
    news5 = cursor5.fetchall()[:5]
    # 兩岸
    return render(request, "news-2.html", {'News4': news4, 'News5': news5})


def news3(request):
    cursor6 = connection.cursor()
    cursor7 = connection.cursor()
    cursor6.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['6'])
    cursor7.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['7'])
    news6 = cursor6.fetchall()[:5]
    news7 = cursor7.fetchall()[:5]

    # 國際
    return render(request, "news-3.html", {'News6': news6, 'News7': news7})


def news4(request):
    cursor8 = connection.cursor()
    cursor9 = connection.cursor()

    cursor8.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['8'])
    cursor9.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['9'])
    news8 = cursor8.fetchall()[:5]
    news9 = cursor9.fetchall()[:5]

    # 產業
    return render(request, "news-4.html", {'News8': news8, 'News9': news9})


def news5(request):
    cursor10 = connection.cursor()
    cursor11 = connection.cursor()
    cursor10.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['10'])
    cursor11.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['11'])
    news10 = cursor10.fetchall()[:5]
    news11 = cursor11.fetchall()[:5]
    # 理財
    return render(request, "news-5.html", {'News10': news10, 'News11': news11})


def newssearch(request):
#     cursor0 = connection.cursor()
#     cursor0.execute("select newsid,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s",['1'])
#     news0 = cursor0.fetchall()[:5]
#     paginator=Paginator(news0,5)
#     try:
#         current_page=request.GET.get("page",1) #  http://127.0.0.1:8000/index/?page=20
#         news=paginator.page(current_page)
#     except (EmptyPage,PageNotAnInteger):
#         news=paginator.page(1)

#     return render(request,'news.html',{'News':news})

# def doc_main(request):
#     doc_all = News.objects.all().order_by("newsid")
#     limit = 20
#     page = request.GET.get('page', 1)
#     paginator = Paginator(doc_all, limit)
#     try:
#         newsid = paginator.page(page)
#     except PageNotAnInteger:
#         newsid = paginator.page(1)
#     except EmptyPage:
#         newsid = paginator.page(paginator.num_pages)
#     context = {
#         'newsid': newsid,
#     }
#     return render(request, 'news.html', context)

# def doc_user_list(request):
#     user = request.user
#     doc_filter = News.objects.filter(user_id=user.id).order_by("id")
#     limit = 5
#     page = request.GET.get('page', 1)
#     paginator = Paginator(doc_filter, limit)
#     try:
#         newsid = paginator.page(page)
#     except PageNotAnInteger:
#         newsid = paginator.page(1)
#     except EmptyPage:
#         newsid = paginator.page(paginator.num_pages)
#     context = {
#         'newsid': newsid,
#     }
   return render(request, "news-search.html", locals())


#--------------------討論版---------------------------
def forum(request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
    return render(request,"forum.html",locals())

#--------------------討論版撰寫---------------------------
def forumwrite (request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
    return render(request,"forum-write.html",locals())

#--------------------討論版內容---------------------------
def forumcontent (request):
    if 'username' in request.session:
        ok ='yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
    return render(request,"forum-content.html",locals())

