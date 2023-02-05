import os
import uuid

from django.db import models
from django import forms

from customers.models import Customers


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("pictures", filename)


# Create your models here.
class Rooms(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    room_type = models.CharField(max_length=20)  # 房间类型：单人间、双人房、大床房
    room_num = models.IntegerField()  # 房间号
    room_cover_pic = models.FileField(upload_to=user_directory_path, verbose_name="图片", null=True)  # 房间封面图片
    introduction = models.CharField(max_length=1024)  # 房间简介
    is_occupied = models.BooleanField()  # 房间是否被占用 0：否 1：是
    price = models.FloatField()  # 房间定价

    class Meta:
        db_table = 'rooms'


# 定义用户表的表单用户创建用户等
class RoomsForm(forms.ModelForm):
    class Meta:
        model = Rooms
        exclude = ['id']
        widgets = {
            'room_cover_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["jpg", "png"]:
            raise forms.ValidationError("Only jpg and pdf files are allowed.")

        return file


# 房间详情
class RoomDetails(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    room_id = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)  # 房间id关联
    room_pic = models.FileField(upload_to=user_directory_path, verbose_name="图片", null=True)  # 房间内部图片
    describe = models.CharField(max_length=1024)  # 描述

    class Meta:
        db_table = 'room_details'


class RoomDetailsForm(forms.ModelForm):
    class Meta:
        model = RoomDetails
        exclude = ['id', 'room_id']
        widgets = {
            'room_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["jpg", "png"]:
            raise forms.ValidationError("Only jpg and png files are allowed.")

        return file


# 房间入住管理以及预定信息
class RoomCheckIns(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    room_id = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)  # 房间id关联
    customer_id = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)  # 顾客id关联
    start_time = models.DateField(auto_now=False)  # 房间使用开始时间
    end_time = models.DateField(auto_now=False)  # 房间使用结束时间
    days = models.IntegerField()  # 房间使用天数
    is_confirmed = models.BooleanField()  # 房间是否确认办理入住 0：否 1：是
    check_time = models.DateTimeField(auto_now=False, null=True)  # 退房时间
    state = models.IntegerField(default=0)  # 房间是否确认办理退房 0：未退房 1：订单被取消 2：已退房

    class Meta:
        db_table = 'room_checkins'


# 房间入住管理入住顾客
class RoomCheckInCustomers(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    room_checkin_id = models.ForeignKey(RoomCheckIns, on_delete=models.DO_NOTHING, null=True)  # 房间id关联
    customer_id = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)  # 顾客id关联
    name = models.CharField(max_length=20)  # 顾客姓名

    class Meta:
        db_table = 'room_checkin_customers'
        unique_together = ['room_checkin_id', 'customer_id']
