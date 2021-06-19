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
    cursor = get_corsor()
    cursor.execute("select id,name,author from book")
    books = cursor.fetchall()
    return render(request, 'index.html', context={"books": books})


def add_book(request):
    if request.method == 'GET':
        return render(request,'add_book.html')
    else:
        name = request.POST.get("name")
        author = request.POST.get("author")
        book_id = random.randint(0, 1000)
        cursor = get_corsor()
        cursor.execute("insert into book(id,name,author) values('%d','%s','%s')" % (book_id,name,author))
        # 跳转到首页
        return redirect(reverse('index'))


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
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print ("fuck ",username,password)
            cursor = get_corsor()
            cursor.execute("select user_password from WebUser where user_name='%s'" % (username))
            FoundPassword=cursor.fetchall()
            print(FoundPassword[0][0])
            try:
                print("entered try")
                #FoundPassword=cursor.execute("select user_password from WebUser where user_name='%s'" % (username))
                if FoundPassword[0][0] == password:
                    return redirect('/index/')
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
            cursor = get_corsor()
            cursor.execute("insert into WebUser(user_id,user_name,user_password) values('%d','%s','%s')" % (random.randint(0,1000),username,password))
            print("execute achieved")
        return render(request, 'register.html', locals())

    register_form = UserForm()
    return render(request, 'register.html')

def logout(request):
    pass
    return redirect('/index/')

