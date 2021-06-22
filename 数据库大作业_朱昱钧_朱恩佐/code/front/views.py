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
        if owner==1:
            user_videos=models.Video.objects.filter()
        else:
            user_videos=models.Video.objects.filter(user_id_id=owner)
        print(owner)
        shared_video_temp = models.Share.objects.filter(user2_id_id=owner).all()
        shared_videos = []
        for temp in shared_video_temp:
            shared_videos.extend(list(models.Video.objects.filter(video_id=temp.video_id_id)))

        print(shared_videos)

        return render(request,'user_home.html',locals())

    elif request.method == 'POST':
        if request.POST.get('upload'):
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
            newurl='/video/'+request.POST.get("id")
            return redirect(newurl,locals())
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
        elif request.POST.get('share'):
            print("entered share")
            owner = request.session['user_id']
            id=request.POST.get("id")
            target_user=request.POST.get("user")
            try:
                origin_user=models.WebUser.objects.get(user_id=owner)
                origin_user_id=origin_user.user_id
                target_user=models.WebUser.objects.get(user_name=target_user)
                print(1)
                target_user_id=target_user.user_id
                print(2)
                new_share=models.Share.objects.create(user1_id_id=origin_user_id,user2_id_id=target_user_id,video_id_id=id)
                print(3)
                print("share saved")
            except:
                print("share failed")
                message="分享出现错误，请检查目标用户名"
            user_videos=models.Video.objects.filter(user_id_id=owner)
            return render(request,'user_home.html',locals())
        else:
            return render(request,'user_home.html',locals())

def view(request):
    if request.method=='GET':
        cur_url=str(request.path)
        splited_url=cur_url.split('/')
        id=splited_url[-1]
        video=models.Video.objects.get(video_id=id)
        comments=models.Comment.objects.filter(video_id_id=id)
        return render(request,'video.html',locals())
    else:
        if request.POST.get('upload'):
            cur_url=str(request.path)
            splited_url=cur_url.split('/')
            id=splited_url[-1]
            video=models.Video.objects.get(video_id=id)
            comment = request.POST.get("comment")
            owner = request.session['user_id']
            new_comment = models.Comment.objects.create(user_id_id=owner,video_id_id=id)
            new_comment.comment_word = comment
            new_comment.save()
            comments=models.Comment.objects.filter(video_id_id=id)
        # 跳转到首页
            return render(request,'video.html',locals())
        else:
            print("entered delete")
            id=request.POST.get("id")
            comment=models.Comment.objects.get(comment_id=id)
            user=request.session['user_id']
            if user==1 or user==comment.user_id:
                print("delete enabled")
                models.Comment.objects.filter(comment_id=id).delete();
            else:
                print("delete disabled")
            owner = request.session['user_id']
            comments=models.Comment.objects.filter(video_id_id=id)
            return render(request,'video.html',locals())



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
            user=models.WebUser.objects.get(user_name=username)
            print(user)
            print(user.user_password)
            try:
                print("entered try")
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

