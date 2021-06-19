from django.shortcuts import render
from django.db import connection
import random
from django.shortcuts import redirect
from django.shortcuts import reverse

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
