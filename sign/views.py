from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sign.models import *


# Create your views here.
# 首页(登录)
def index(request):
    return render(request, 'index.html')


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            response = HttpResponseRedirect('/event_manage/')  # 添加浏览器cookie
            # response.set_cookie('user',username,3600)#添加session
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 退出动作
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response


# 发布会管理（登录之后默认页面）
@login_required
def event_manage(request):
    username = request.session.get('user', '')
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 2)  # 把查询出来的所有嘉宾列表guest_list放到Paginator类中，划分每页显示2条数据
    page = request.GET.get('page')  # 通过GET请求得到当前要现实第几页的数据
    try:
        event_list = paginator.page(page)  # 获取第page页的数据
    except PageNotAnInteger:
        event_list = paginator.page(1)  # 如果page不是整数，取第一页面数据
    except EmptyPage:
        event_list = paginator.page(paginator.num_pages)  # 如果page不在范围内，取最后一页面数据
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    paginator = Paginator(event_list, 2)  # 把查询出来的所有嘉宾列表guest_list放到Paginator类中，划分每页显示2条数据
    page = request.GET.get('page')  # 通过GET请求得到当前要现实第几页的数据
    try:
        event_list = paginator.page(page)  # 获取第page页的数据
    except PageNotAnInteger:
        event_list = paginator.page(1)  # 如果page不是整数，取第一页面数据
    except EmptyPage:
        event_list = paginator.page(paginator.num_pages)  # 如果page不在范围内，取最后一页面数据
    return render(request, "event_manage.html", {"user": username, "events": event_list, "search_name": search_name})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()  # 获取Guest全部数据对象
    paginator = Paginator(guest_list, 2)  # 把查询出来的所有嘉宾列表guest_list放到Paginator类中，划分每页显示2条数据
    page = request.GET.get('page')  # 通过GET请求得到当前要现实第几页的数据
    try:
        contacts = paginator.page(page)  # 获取第page页的数据
    except PageNotAnInteger:
        contacts = paginator.page(1)  # 如果page不是整数，取第一页面数据
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 如果page不在范围内，取最后一页面数据
    # 通过render()方法附加在guest_manage.html页面返回给客户端
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 嘉宾名称搜索
@login_required
def search_realname(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get("realname", "")
    # 注意这里需要将过滤器的名称也修改为realname__contains
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    paginator = Paginator(guest_list, 2)  # 把查询出来的所有嘉宾列表guest_list放到Paginator类中，划分每页显示2条数据
    page = request.GET.get('page')  # 通过GET请求得到当前要现实第几页的数据
    try:
        contacts = paginator.page(page)  # 获取第page页的数据
    except PageNotAnInteger:
        contacts = paginator.page(1)  # 如果page不是整数，取第一页面数据
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # 如果page不在范围内，取最后一页面数据
    # 通过render()方法附加在guest_manage.html页面返回给客户端
    return render(request, "guest_manage.html",
                  {"user": username, "guests": contacts, "search_realname": search_realname})


# 签到
@login_required
def sign_index(request, eid):
    username = request.session.get('user', '')
    print(username)
    event = get_object_or_404(Event, id=eid)
    guest_list = len(get_list_or_404(Guest, event_id=eid))
    guest_sign = len(get_list_or_404(Guest, event_id=eid, sign=1))
    return render(request, 'sign_index.html',
                  {"user": username, "event": event, 'guest_list': guest_list, 'guest_sign': guest_sign})


# 签到动作
@login_required
def sign_index_action(request, eid):
    username = request.session.get('user', '')
    event = get_object_or_404(Event, id=eid)
    guest_list = len(get_list_or_404(Guest, event_id=eid))
    guest_sign = len(get_list_or_404(Guest, event_id=eid, sign=1))
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html',
                      {'user': username, 'event': event, 'hint': 'phone error.', 'guest_list': guest_list,
                       'guest_sign': guest_sign})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html',
                      {'user': username, 'event': event, 'hint': 'event id or phone error.', 'guest_list': guest_list,
                       'guest_sign': guest_sign})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html',
                      {'user': username, 'event': event, 'hint': 'user has sign in.', 'guest_list': guest_list,
                       'guest_sign': guest_sign})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        guest_sign = guest_sign + 1
        return render(request, 'sign_index.html',
                      {'user': username, 'event': event, 'hint': 'sign in success!', 'guest': result,
                       'guest_list': guest_list, 'guest_sign': guest_sign})
