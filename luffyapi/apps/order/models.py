from django.db import models
from user.models import User
from course.models import Course


class Order(models.Model):
    """订单模型"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )
    pay_choices = (
        (1, '支付宝'),
        (2, '微信支付'),
    )
    subject = models.CharField(verbose_name="订单标题", help_text='订单标题', max_length=150)
    total_amount = models.DecimalField(verbose_name="订单总价", max_digits=10, decimal_places=2, default=0)
    out_trade_no = models.CharField(verbose_name="订单号", max_length=64, unique=True)
    trade_no = models.CharField(verbose_name="流水号", max_length=64, null=True)
    order_status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices, default=0)
    pay_type = models.SmallIntegerField(verbose_name="支付方式", choices=pay_choices, default=1)
    pay_time = models.DateTimeField(verbose_name="支付时间", null=True)
    user = models.ForeignKey(verbose_name="下单用户", to=User, related_name='order_user', on_delete=models.DO_NOTHING,
                             db_constraint=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = "luffy_order"
        verbose_name = "订单记录"
        verbose_name_plural = "订单记录"

    def __str__(self):
        return f"{self.subject} - ￥{self.total_amount}"

    @property
    def courses(self):
        data_list = []
        for item in self.order_courses.all():
            data_list.append({
                "id": item.id,
                "course_name": item.course.name,
                "real_price": item.real_price,
            })
        return data_list


class OrderDetail(models.Model):
    """订单详情"""
    order = models.ForeignKey(verbose_name="订单", to=Order, related_name='order_courses', on_delete=models.CASCADE, db_constraint=False)
    course = models.ForeignKey(verbose_name="课程", help_text='课程id', to=Course, related_name='course_orders', on_delete=models.CASCADE,
                               db_constraint=False)
    price = models.DecimalField(verbose_name="课程原价", max_digits=6, decimal_places=2)
    real_price = models.DecimalField(verbose_name="课程实价", max_digits=6, decimal_places=2)

    class Meta:
        db_table = "luffy_order_detail"
        verbose_name = "订单详情"
        verbose_name_plural = "订单详情"

    def __str__(self):
        try:
            return f"商品: {self.course.name} 订单号：{self.order.out_trade_no}"
        except:
            return super().__str__()

