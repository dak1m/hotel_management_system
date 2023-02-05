from django.db import models

StateDesc = {
    1: "已下单",
    2: "已取消",
    3: "已完成",
}

DescState = {
    "已下单": 1,
    "已取消": 2,
    "已完成": 3,
}


# Create your models here.
class Orders(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    order_no = models.CharField(max_length=20)  # 订单号
    customer_id = models.ForeignKey('customers.Customers', on_delete=models.DO_NOTHING)  # 房间是否确认办理入住 0：否 1：是
    room_checkin_id = models.ForeignKey('rooms.RoomCheckIns', on_delete=models.CASCADE)  # 房间id
    price = models.FloatField()  # 订单金额
    state = models.IntegerField()  # 订单状态: 1：已下单 2：已取消 3：已完成
    finish_time = models.DateTimeField(null=True)  # 完成时间

    class Meta:
        db_table = 'orders'
