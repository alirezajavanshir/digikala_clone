from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from extensions.utils import upload_image_path

User = get_user_model()


class UserProfile(models.Model):
    """
    مدل پروفایل کاربر
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="کاربر", related_name="profile"
    )
    phone = models.CharField(blank=True, max_length=20, verbose_name="تلفن")
    national_code = models.CharField(
        blank=True, max_length=20, verbose_name="کد ملی", default="_"
    )
    image = models.ImageField(
        blank=True, null=True, upload_to=upload_image_path, verbose_name="تصویر"
    )

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"

    def __str__(self):
        return self.user.username

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')

    image_tag.short_description = "تصویر"


class UserAddress(models.Model):
    """
    مدل آدرس کاربر
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    full_name = models.CharField(
        blank=True, max_length=60, verbose_name="نام و نام خانوادگی"
    )
    phone = models.CharField(blank=True, max_length=20, verbose_name="تلفن")
    ostan = models.CharField(blank=True, max_length=20, verbose_name="استان")
    city = models.CharField(blank=True, max_length=20, verbose_name="شهر")
    address = models.CharField(blank=True, max_length=150, verbose_name="آدرس پستی")
    post_code = models.IntegerField(blank=True, verbose_name="کد پستی", null=True)
    selected = models.BooleanField(default=False, verbose_name="آدرس منتخب")

    class Meta:
        verbose_name = "آدرس کاربر"
        verbose_name_plural = "آدرس‌های کاربران"

    def __str__(self):
        return self.user.username


class History(models.Model):
    """
    مدل تاریخچه بازدید
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    viewed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تاریخ بازدید"
        verbose_name_plural = "تاریخچه بازدیدها"

    def __str__(self):
        return f"{self.content_object} در تاریخ {self.viewed_on}"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    ایجاد توکن احراز هویت برای کاربر جدید
    """
    if created:
        Token.objects.create(user=instance)
