from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from extensions.utils import upload_image_path


class Category(MPTTModel):
    """
    مدل دسته‌بندی‌ها
    """

    STATUS = (("True", "فعال"), ("False", "غیرفعال"))

    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.SET_NULL,
        verbose_name="دسته‌مادر",
    )
    title = models.CharField(max_length=50, verbose_name="عنوان")
    en_title = models.CharField(max_length=50, verbose_name="عنوان انگلیسی")
    keyword = models.CharField(max_length=250, verbose_name="کلمه کلیدی")
    description = models.CharField(max_length=300, verbose_name="توضیحات")
    status = models.CharField(max_length=50, choices=STATUS, verbose_name="وضعیت")
    image = models.ImageField(
        blank=True, upload_to=upload_image_path, verbose_name="تصویر"
    )
    slug = models.SlugField(
        verbose_name="عبارت لینک", unique=True, allow_unicode=True, max_length=200
    )
    creat_at = models.DateTimeField(
        auto_now_add=True, verbose_name="ایجاد شده در تاریخ"
    )
    update_at = models.DateTimeField(auto_now=True, verbose_name="آپدیت شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته"
        verbose_name_plural = "دسته‌بندی‌ها"

    class MPTTMeta:
        order_insertion_by = ["title"]

    def get_absolute_url(self):
        """
        دریافت URL مطلق دسته‌بندی
        """
        return reverse("product_category_list", kwargs={"slug": self.slug})
