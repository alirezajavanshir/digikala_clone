from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from product.models import Product
from variant.models import Variants
from extensions.utils import jalali_converter


class PostWay(models.Model):
    way = models.CharField(max_length=60, verbose_name="روش سفارش")
    price = models.IntegerField(verbose_name="هزینه ارسال")
    selected = models.BooleanField(default=False, verbose_name="روش پست منتخب")

    class Meta:
        verbose_name = "روش‌‌ ارسال"
        verbose_name_plural = "روش‌های ارسال"

    def __str__(self):
        return self.way


class ShopCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="کاربر"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, verbose_name="محصول"
    )
    variant = models.ForeignKey(
        Variants,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="مدل محصول",
    )
    quantity = models.IntegerField(verbose_name="تعداد")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        return self.product.title or "محصول بدون عنوان"

    @property
    def price(self):
        return f"{self.variant.price if self.variant else self.product.price:,} تومان"

    @property
    def amount(self):
        return self.quantity * (
            self.variant.price if self.variant else self.product.price
        )


class Order(models.Model):
    STATUS = (
        ("New", "جدید"),
        ("Accepted", "تایید سفارش"),
        ("Preparing", "آماده سازی سفارش"),
        ("OutCompany", "خروج از مرکز پردازش"),
        ("InPostOffice", "تحویل به پست"),
        ("OnShipping", "مرکز مبادلات پست"),
        ("Arrive", "تحویل به مشتری"),
        ("Canceled", "لغو شده"),
    )
    PAY_WAY = (("online", "پرداخت آنلاین"), ("creditCard", "کیف پول اعتباری"))

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="کاربر"
    )
    code = models.CharField(max_length=10, editable=False, verbose_name="کد سفارش")
    address_full_name = models.CharField(
        blank=True, max_length=60, verbose_name="نام و نام خانوادگی"
    )
    address_phone = models.CharField(blank=True, max_length=20, verbose_name="تلفن")
    address_ostsn = models.CharField(blank=True, max_length=20, verbose_name="استان")
    address_city = models.CharField(blank=True, max_length=20, verbose_name="شهر")
    address_address = models.CharField(
        blank=True, max_length=150, verbose_name="آدرس پستی"
    )
    address_post_code = models.IntegerField(
        blank=True, null=True, verbose_name="کد پستی"
    )
    post_way = models.ForeignKey(
        PostWay, on_delete=models.SET_NULL, null=True, verbose_name="نحوه ارسال"
    )
    pay_way = models.CharField(
        max_length=50, choices=PAY_WAY, default="online", verbose_name="نحوه پرداخت"
    )
    total = models.IntegerField(verbose_name="جمع مبلغ کل سفارشات")
    amount = models.IntegerField(verbose_name="جمع تعداد کل سفارشات")
    status = models.CharField(
        max_length=30, choices=STATUS, default="New", verbose_name="وضعیت"
    )
    ip = models.CharField(blank=True, max_length=20, verbose_name="آی‌پی")
    admin_note = models.CharField(
        blank=True, max_length=100, verbose_name="یادداشت ادمین"
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده")
    update_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return self.user.first_name if self.user else "کاربر ناشناس"

    @property
    def user_name(self):
        return (
            f"{self.user.first_name} {self.user.last_name} ( {self.user.username} )"
            if self.user
            else "کاربر ناشناس"
        )

    @property
    def total_th(self):
        return f"{self.total:,}" if self.total is not None else "0"

    @property
    def post_w(self):
        return self.post_way.way if self.post_way else "نامشخص"

    @property
    def post_p(self):
        return f"{self.post_way.price:,}" if self.post_way else "نامشخص"

    @property
    def j_create_at(self):
        return jalali_converter(self.create_at)

    @property
    def j_update_at(self):
        return jalali_converter(self.update_at)


class OrderProduct(models.Model):
    STATUS = (
        ("New", "جدید"),
        ("Accepted", "تایید سفارش"),
        ("Canceled", "کنسل سفارش"),
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="سفارش", related_name="order"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="کاربر"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, verbose_name="محصول"
    )
    variant = models.ForeignKey(
        Variants,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="مدل محصول",
    )
    quantity = models.IntegerField(verbose_name="تعداد")
    price = models.IntegerField(verbose_name="قیمت")
    amount = models.IntegerField(verbose_name="قیمت کل")
    status = models.CharField(
        max_length=30, choices=STATUS, default="New", verbose_name="وضعیت"
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده")
    update_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")

    class Meta:
        verbose_name = "سفارش محصول"
        verbose_name_plural = "سفارشات محصولات"

    def __str__(self):
        return (
            self.variant.title
            if self.variant
            else self.product.title or "محصول بدون عنوان"
        )

    @property
    def price_th(self):
        return f"{self.price:,}"

    @property
    def productt(self):
        return self.variant.title if self.variant else self.product.title

    @property
    def size(self):
        return self.variant.size if self.variant else "-"

    @property
    def color(self):
        return self.variant.color if self.variant else "-"

    @property
    def amount_th(self):
        return f"{self.amount:,}"

    def image_tag(self):
        return mark_safe(
            f'<img src="{self.product.image.url}" height="50" alt="{self.product.title}"/>'
        )

    image_tag.short_description = "تصویر"

    @property
    def j_create_at(self):
        return jalali_converter(self.create_at)

    @property
    def j_update_at(self):
        return jalali_converter(self.update_at)
