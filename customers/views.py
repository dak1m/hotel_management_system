import csv
from datetime import datetime

from django.contrib import messages
from django.template.defaultfilters import register

from .models import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
@login_required
def list_customers(request):
    customers = Customers.objects.all()
    name = request.GET.get("name")
    cellphone = request.GET.get("cellphone")
    print(name)
    print(cellphone)
    param = ""
    if name is not None and name != "":
        customers = customers.filter(name__istartswith=name)
        param += "&name={}".format(name)
    if cellphone is not None and cellphone != "":
        customers = customers.filter(cellphone__istartswith=cellphone)
        param += "&cellphone={}".format(cellphone)

    paginator = Paginator(customers, 10)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "customers/customers.html",
                  {"customers": page_obj,
                   "param": param,
                   "user": request.user.username})


@register.filter('list')
def do_list(value):
    return range(1, value + 1)


@login_required
def create_customer(request):
    if request.method == "POST":
        customer = CustomersForm(request.POST)
        print(customer.errors)
        if customer.is_valid():
            customer.save()
            messages.success(request, '添加用户成功')
            return redirect("list_customers")
        else:
            messages.error(request, '添加用户失败')

    return render(request, "customers/create_customer.html", {"user": request.user.username})


@login_required
def update_customer(request, pk):
    obj = get_object_or_404(Customers, pk=pk)
    if request.method == "POST":
        customer = CustomersForm(data=request.POST, instance=obj)
        if customer.is_valid():
            customer.save()
            messages.success(request, '更新用户成功')
            return render(request, "customers/update_customer.html", {'customer': obj, "user": request.user.username})
        else:
            messages.error(request, '更新用户失败')

    return render(request, "customers/update_customer.html", {'customer': obj, "user": request.user.username})


@login_required
def delete_customer(request, pk):
    obj = get_object_or_404(Customers, pk=pk)
    obj.delete()
    return redirect("list_customers")


@login_required
def load_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    # 指定导出文件的格式
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'name',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        ['姓名', '性别', '手机号', '身份证号码', '备注信息']
    )

    customers = Customers.objects.all()
    for customer in customers:
        writer.writerow(
            [customer.id, customer.name, customer.sex, customer.cellphone, customer.identity_card, customer.extra])

    return response


def common_response(message, status):
    resp = {"message": message, "status": status}
    return resp
