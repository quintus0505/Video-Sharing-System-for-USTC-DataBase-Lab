from django.shortcuts import render
from django.db import connection
import random
from django.shortcuts import redirect
from django.shortcuts import reverse
from . import models
from .forms import UserForm

def get_corsor():
    return connection.cursor()


# Create your views here.
def index(request):
    try:
        if request.session['is_login']:
            return redirect('/user_home/')
    except:
        return render(request, 'index.html')


def user_home(request):
    if request.method == 'GET':
        owner = request.session['user_id']
        user_videos=models.Video.objects.filter(user_id_id=owner)
        return render(request,'user_home.html',locals())
    elif request.method == 'POST':
        print("fuck2")
        if request.POST.get('upload'):
            print("fuck")
            name = request.POST.get("name")
            address = request.POST.get("address")
            owner = request.session['user_id']
            new_video = models.Video.objects.create(user_id_id=owner)
            new_video.video_name = name
            new_video.video_address = address
            new_video.save()
        # 跳转到首页
            owner = request.session['user_id']
            user_videos=models.Video.objects.filter(user_id_id=owner)
            return render(request,'user_home.html',locals())
        elif request.POST.get('view'):
            print("entered view")
            return render(request,'video.html',locals())
        elif request.POST.get('delete'):
            print("entered delete")
            id=request.POST.get("id")
            video=models.Video.objects.get(video_id=id)
            user=request.session['user_id']
            if user==1 or user==video.user_id:
                print("delete enabled")
                models.Video.objects.filter(video_id=id).delete();
            else:
                print("delete disabled")
            owner = request.session['user_id']
            user_videos=models.Video.objects.filter(user_id_id=owner)
            return render(request,'user_home.html',locals())
        else:
            return render(request,'user_home.html',locals())


def book_detail(request,book_id):
    pass

def delete_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        cursor = get_corsor()
        cursor.execute("delete from book where id=%s" % book_id)
        return redirect(reverse('index'))
    else:
        raise RuntimeError("删除图书的method错误！")

def login(request):
    if request.session.get('is_login',None):
        return redirect('/user_home/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # print ("fuck ",username,password)
            # cursor = get_corsor()
            # cursor.execute("select user_password from WebUser where user_name='%s'" % (username))
            # FoundPassword=cursor.fetchall()
            # cursor.execute("select user_id from WebUser where user_name='%s'" % (username))
            # id=cursor.fetchall()
            # print(FoundPassword[0][0])
            user=models.WebUser.objects.get(user_name=username)
            print(user)
            print(user.user_password)
            try:
                print("entered try")
                #FoundPassword=cursor.execute("select user_password from WebUser where user_name='%s'" % (username))
                print(username)
                user=models.WebUser.objects.get(user_name=username)
                print(user)
                if user.user_password == password:
                    request.session['is_login']=True
                    request.session['user_id']=user.user_id
                    request.session['user_name']=user.user_name
                    return redirect('/user_home/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.method == "POST":
        register_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            #cursor = get_corsor()
            #cursor.execute("insert into WebUser(user_id,user_name,user_password) values('%d','%s','%s')" % (random.randint(0,1000),username,password))
            #print("execute achieved")
            new_user=models.WebUser.objects.create()
            new_user.user_name=username
            new_user.user_password=password
            new_user.save()
        return render(request, 'register.html', locals())

    register_form = UserForm()
    return render(request, 'register.html')

def logout(request):
    if not request.session.get('is_login',None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')

