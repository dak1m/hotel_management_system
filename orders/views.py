import json
import uuid
import time

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from customers.models import Customers
from orders.models import Orders, DescState, StateDesc
from rooms.models import Rooms, RoomCheckIns


# Create your views here.
# 下单
def order(request, room_id):
    room = get_object_or_404(Rooms, pk=room_id)
    customers = Customers.objects.all()
    if request.method == 'POST':
        param = request.POST
        customer_id = param["customer_id"]
        start_time = param["start_time"]
        end_time = param["end_time"]

        order_no = uuid.uuid4().hex[:8]
        days = (time.mktime(time.strptime(end_time, '%Y-%m-%d')) - time.mktime(
            time.strptime(start_time, '%Y-%m-%d'))) / 3600 / 24
        if days < 0:
            messages.error(request, '下单失败：开始时间不能大于结束时间')
            return redirect("list_rooms")

        customer = get_object_or_404(Customers, pk=customer_id)

        room_checkin = RoomCheckIns.objects.create(
            room_id=room,
            customer_id=customer,
            start_time=start_time,
            end_time=end_time,
            days=days,
            is_confirmed=False,
        )
        # 房间被更新为被占用
        room.is_occupied = True
        room.save()

        # 生成订单号

        Orders.objects.create(
            order_no=order_no,
            customer_id=customer,
            room_checkin_id=room_checkin,
            state=DescState.get('已下单'),
            price=days * room.price,
        )

        messages.success(request, '下单成功')
        return redirect("list_rooms")

    return render(request, 'orders/create_order.html',
                  {"room": room, "customers": customers, "user": request.user.username})


def list_order(request):
    orders = Orders.objects.all()

    return render(request, "orders/orders.html", {"orders": orders,
                                                  "state_desc": StateDesc,
                                                  "user": request.user.username})


# 取消订单
@login_required
@csrf_exempt  # 不做csrf验证
def cancel_order(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        order_id = params["order_id"]

        print(order_id)
        order = get_object_or_404(Orders, pk=order_id)
        order.state = DescState.get("已取消")
        order.save()

        room_checkin = get_object_or_404(RoomCheckIns, pk=order.room_checkin_id.id)
        room_checkin.state = 1
        room_checkin.save()

        room = get_object_or_404(Rooms, pk=order.room_checkin_id.room_id.id)
        room.is_occupied = False
        room.save()

        return JsonResponse({"code": 200, "message": "取消订单成功"})
