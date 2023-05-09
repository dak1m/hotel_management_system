from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# 首页登录
from orders.models import Orders


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # 保存登录会话
            login(request, user)

            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误！'})

    return render(request, 'login.html')


def user_sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and username != 'admin':
            # 保存登录会话
            login(request, user)

            return redirect("/dashboard")
        else:
            return render(request, 'user_login.html', {'error': '用户名或密码错误！'})

    return render(request, 'user_login.html')


@login_required
def log_out(request):
    logout(request)
    return redirect("/")


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {"user": request.user.username})


@login_required
def statistics(request):
    orders = Orders.objects.all()
    pie_labels = []
    pie_data = []
    line_labels = []
    line_data = []
    bar_labels = []
    bar_data = []
    c_bar_labels = []
    c_bar_data = []
    room_type_count = {}
    room_num_count = {}
    finish_time_price = {}
    customer_order = {}
    for order in orders:
        room_type = order.room_checkin_id.room_id.room_type
        room_num = order.room_checkin_id.room_id.room_num
        customer = order.customer_id.name
        if room_type not in room_type_count:
            room_type_count[room_type] = 1
        else:
            room_type_count[room_type] += 1
        if room_num not in room_num_count:
            room_num_count[room_num] = 1
        else:
            room_num_count[room_num] += 1
        if order.finish_time is not None:
            finish_date = order.finish_time.strftime('%Y-%m-%d')
            if finish_date not in finish_time_price:
                finish_time_price[finish_date] = order.price
            else:
                finish_time_price[finish_date] += order.price
        if customer not in customer_order:
            customer_order[customer] = 1
        else:
            customer_order[customer] += 1
    for k, v in room_type_count.items():
        pie_labels.append(k)
        pie_data.append(v)
    for k, v in finish_time_price.items():
        line_labels.append(k)
        line_data.append(v)
    for k, v in room_num_count.items():
        bar_labels.append(k)
        bar_data.append(v)
    for k, v in customer_order.items():
        c_bar_labels.append(k)
        c_bar_data.append(v)

    return render(request, 'statistics.html', {'pie_labels': pie_labels, 'pie_data': pie_data,
                                               'line_labels': line_labels, 'line_data': line_data,
                                               'bar_labels': bar_labels, 'bar_data': bar_data,
                                               'c_bar_labels': c_bar_labels, 'c_bar_data': c_bar_data,
                                               "user": request.user.username})
