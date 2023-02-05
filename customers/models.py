from django.db import models
from django import forms


# Create your models here.

# 用户信息表
class Customers(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    name = models.CharField(max_length=20)  # 姓名
    sex = models.CharField(max_length=2)  # 性别
    cellphone = models.CharField(max_length=20)  # 手机号
    identity_card = models.CharField(max_length=20)  # 身份证号码
    extra = models.CharField(max_length=1024, blank=True)  # 备注信息

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customers'


# 定义用户表的表单用户创建用户等
class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ['id']
