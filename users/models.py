from django.db import models


# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    email = models.CharField(max_length=20)  # 邮件
    password = models.CharField(max_length=20)  # 密码
    cellphone = models.CharField(max_length=20)  # 手机号

    def __str__(self):
        return self.email