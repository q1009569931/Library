from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Books, User, Collection
from .form import RegisterForm, searchForm, LoginForm
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
# Create your views here.


def index(request):
    form = searchForm()
    content = {'user': request.user, 'searchForm': form}
    return render(request, 'library/index.html', content)


def search(request):
    form = searchForm()
    search_by = request.GET.get('search_by')
    keyword = request.GET.get('keyword')
    # 获取url路径（带参数的）
    current_path = request.get_full_path()

    books = Books.objects.all()
    if search_by == 'ISBN':
        books = books.filter(ISBN=keyword)
    elif search_by == '书名':
        books = books.filter(title__contains=keyword)
    else:
        books = books.filter(author__contains=keyword)

    # 分页
    page = request.GET.get('page', default='1')
    books = Paginator(books, 5)
    try:
        books = books.page(page)
    except PageNotAnInteger:
        books = books.page(1)
    except EmptyPage:
        # deliver last page of results
        books = books.page(books.num_pages)

    content = {
        'user': request.user, 
        'searchForm': form, 
        'search_by': search_by,
        'keyword': keyword,
        'books': books,
        'current_path': current_path
    }

    return render(request, 'library/search.html', content)

def login(request):
    state = None
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['userid']
            password = loginForm.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('/library/index/')
                else:
                    state = 'user_state_unature'
            else:
                state = 'error'
        else:
            state = 'error'
    else:
        loginForm = LoginForm()

    content = {'state':state, 'loginForm':loginForm}
    return render(request, 'library/login.html', content)

def register(request):
    state = None
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        form = RegisterForm(request.POST)
        if not userid or not password:
            state = 'empty'
        elif 6 > len(userid) or len(userid) > 20:
            state = 'userid_len_error'
        elif 6 > len(password) or len(password) > 20:
            state = 'password_len_error'
        elif password != repassword:
            state = 'repeat_error'
        elif User.objects.filter(username=userid):
            state = 'user_exist'
        else:
            u = User()
            u.username = userid
            u.set_password(password)
            # u.password = password， 区别在于上面这句会加密，下面这句不会。
            u.email = email
            u.last_name = nickname
            u.save()
            state = 'success'
    else:
        form = RegisterForm()
    return render(request, 'library/register.html', {'registerForm': form, 'state':state})

def logout(request):
    auth.logout(request)
    return redirect('/library/index/')

def detail(request):
    state = None
    ISBN = request.GET.get('ISBN')
    action = request.GET.get('action')
    user = request.user
    try:
        book = Books.objects.get(ISBN=ISBN)
    except Books.DoesNotExist:
        return HttpResponse("无此对象")

    if user.is_authenticated:
        state = 'logined'
        if Collection.objects.filter(userid=user).filter(ISBN=book):
            state = 'collected'
        else:
            state = 'no_collected'
    else:
        state = 'no_user'

    if action == 'collect' and state == 'no_collected':
        collection = Collection.objects.create(userid=user, ISBN=book)
        collection.save()
        state = 'success'

    print(state)
    content = {
        'state':state,
        'book':book,
    }
    return render(request, 'library/book_detail.html', content)
