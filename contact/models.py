from django.db import models
from extensions.utils import jalali_converter


class ContactMessage(models.Model):
    STATUS = (
        ("New", "جدید"),
        ("Read", "خوانده شده"),
        ("Closed", "بسته"),
    )

    name = models.CharField(max_length=50, verbose_name="نام و نام‌خانوادگی", blank=True)
    email = models.EmailField(max_length=50, verbose_name="ایمیل", blank=True)
    subject = models.CharField(max_length=50, verbose_name="موضوع", blank=True)
    message = models.TextField(max_length=255, verbose_name="پیام", blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS, default="New", verbose_name="وضعیت"
    )
    ip = models.GenericIPAddressField(verbose_name="آی‌پی", blank=True, null=True)
    note = models.CharField(max_length=100, verbose_name="یادداشت", blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    update_at = models.DateTimeField(auto_now=True, verbose_name="آخرین آپدیت")

    class Meta:
        verbose_name = "تماس با ما"
        verbose_name_plural = "پیام‌‌های مخاطبین"
        ordering = ["-create_at"]  # ترتیب بر اساس تاریخ ایجاد به صورت نزولی

    def __str__(self):
        return f"{self.subject} - {self.name}" if self.subject else "بدون موضوع"

    def j_create_at(self):
        return jalali_converter(self.create_at)

    j_create_at.short_description = "زمان ارسال"

    def j_update_at(self):
        return jalali_converter(self.update_at)

    j_update_at.short_description = "آخرین آپدیت"
