import json
import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from customers.models import Customers
from orders.models import Orders
from rooms.models import Rooms, RoomsForm, RoomCheckInCustomers, RoomCheckIns, RoomDetailsForm, RoomDetails
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.
# 展示所有房间
@login_required
def list_rooms(request):
    rooms = Rooms.objects.all()
    room_num = request.GET.get("room_num")
    is_occupied = request.GET.get("is_occupied")
    if room_num is not None and room_num != "":
        rooms = rooms.filter(room_num__istartswith=room_num)
    if is_occupied is not None and is_occupied != "":
        rooms = rooms.filter(is_occupied=is_occupied)

    return render(request, "rooms/rooms.html", {"rooms": rooms, "user": request.user.username})


# 展示房间明细
@login_required
def list_room_details(request, room_id):
    room_details = RoomDetails.objects.filter(room_id=room_id)
    is_blank = False
    if len(room_details) == 0:
        is_blank = True
        return redirect("create_room_detail", room_id)
    return render(request, "rooms/room_details.html",
                  {"room_details": room_details, "is_blank": is_blank, "user": request.user.username})


# 创建房间
@login_required
def create_rooms(request):
    if request.method == "POST":
        room = RoomsForm(request.POST, request.FILES)
        print(room.errors)
        if room.is_valid():
            room.save()
            messages.success(request, '添加房间成功')
            return render(request, "rooms/create_room.html", {"user": request.user.username})
        else:
            messages.info(request, '添加房间失败')

    return render(request, "rooms/create_room.html", {"user": request.user.username})


# 创建房间明细
@login_required
def create_room_detail(request, pk):
    if request.method == "POST":
        room = get_object_or_404(Rooms, pk=pk)
        room_detail = RoomDetails(room_id=room)
        room_detail_form = RoomDetailsForm(request.POST, request.FILES, instance=room_detail)
        print(room_detail_form.errors)
        if room_detail_form.is_valid():
            room_detail_form.save()
            messages.success(request, '添加房间明细成功')
            return render(request, "rooms/create_room_detail.html", {"user": request.user.username})
        else:
            messages.info(request, '添加房间明细失败')

    return render(request, "rooms/create_room_detail.html", {"user": request.user.username})


@login_required
def list_room_checkins(request):
    room_checkins = RoomCheckIns.objects.all()
    customers = Customers.objects.all()

    return render(request, "rooms/room_checkins.html",
                  {"room_checkins": room_checkins, "customers": customers, "user": request.user.username})


# 办理入住
@login_required
@csrf_exempt  # 不做csrf验证
def check_in(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        customer_ids = params["customer_ids"]
        room_checkin_id = params["room_checkin_id"]
        # 去重
        customer_ids = list(set(customer_ids))

        room_checkin = get_object_or_404(RoomCheckIns, pk=room_checkin_id)
        for customer_id in customer_ids:
            customer = get_object_or_404(Customers, pk=customer_id)
            obj = RoomCheckInCustomers.objects.create(
                room_checkin_id=room_checkin,
                customer_id=customer,
                name=customer.name,
            )
        room_checkin.is_confirmed = True
        room_checkin.save()

        order = get_object_or_404(Orders, room_checkin_id=room_checkin_id)
        order.finish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        order.save()

        return JsonResponse({"code": 200, "message": "办理入住成功"})


# 展示退房房间信息
@login_required
def list_room_checkouts(request):
    objs = RoomCheckIns.objects.all()

    return render(request, "rooms/room_checkout.html", {'rooms': objs, "user": request.user.username})


# 退房处理
@login_required
@csrf_exempt  # 不做csrf验证
def check_out(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        room_checkin_id = params["room_checkin_id"]
        print(room_checkin_id)

        room_checkin = get_object_or_404(RoomCheckIns, pk=room_checkin_id)
        room_checkin.state = 2
        room_checkin.check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        room_checkin.save()

        room = get_object_or_404(Rooms, pk=room_checkin.room_id.id)
        room.is_occupied = False
        room.save()

        return JsonResponse({"code": 200, "message": "办理退房成功"})


@login_required
def list_checkin_customers(request):
    objs = RoomCheckInCustomers.objects.all().order_by("room_checkin_id")
    id_map_num = {}
    for v in objs:
        if v.room_checkin_id in id_map_num:
            id_map_num[v.room_checkin_id] += 1
        else:
            id_map_num[v.room_checkin_id] = 1
    # 做一个排序，并且需要区分合并的表格
    td1 = '<td rowspan="{}">{}</td>'
    td2 = '<td rowspan="{}">{}</td>'
    td3 = '<td>{}</td>'
    td4 = '<td>{}</td>'
    html = ""
    dom_duplicate = {}
    for v in objs:
        html += '<tr>'
        if v.room_checkin_id not in dom_duplicate:
            html += td1.format(id_map_num[v.room_checkin_id], v.room_checkin_id.id)
            html += td2.format(id_map_num[v.room_checkin_id], v.room_checkin_id.room_id.room_num)
            html += td3.format(v.name)
            html += td4.format(state_dict_name[v.room_checkin_id.state])
            dom_duplicate[v.room_checkin_id] = True
        else:
            html += td3.format(v.name)
            html += td4.format(state_dict_name[v.room_checkin_id.state])
        html += '</tr>'
        print(html)

    return render(request, "rooms/room_checkin_customers.html",
                  {'checkin_customers': objs, 'html': html, "user": request.user.username})


state_dict_name = {
    0: '未退房',
    1: '订单已取消',
    2: '已退房',
}
