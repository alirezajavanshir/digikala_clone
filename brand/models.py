from django.db import models
from django.urls import reverse
from extensions.utils import upload_image_path


class Brand(models.Model):
    """
    مدل برندها
    """

    title = models.CharField(max_length=50, verbose_name="برند")
    title_eng = models.CharField(max_length=150, verbose_name="عنوان انگلیسی")
    keyword = models.CharField(max_length=250, verbose_name="کلمه کلیدی")
    description = models.CharField(max_length=300, verbose_name="توضیحات")
    image = models.ImageField(
        blank=True, upload_to=upload_image_path, verbose_name="تصویر"
    )
    slug = models.SlugField(
        verbose_name="عبارت لینک", unique=True, allow_unicode=True, max_length=200
    )
    creat_at = models.DateTimeField(
        auto_now_add=True, verbose_name="ایجاده شده در تاریخ"
    )
    update_at = models.DateTimeField(auto_now=True, verbose_name="آپدیت شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def get_absolute_url(self):
        """
        دریافت URL مطلق برند
        """
        return reverse("product_brand_list", kwargs={"slug": self.slug})
