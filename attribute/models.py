from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from product.models import Product


class Attrs(models.Model):
    """
    مدل ویژگی‌ها
    """

    title = models.CharField(max_length=60, verbose_name="ویژگی")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"


class AttrProduct(models.Model):
    """
    مدل ویژگی‌های محصول
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attrs", verbose_name="محصول"
    )
    title = models.ForeignKey(
        Attrs, on_delete=models.CASCADE, verbose_name="عنوان ویژگی"
    )
    rate = models.IntegerField(
        verbose_name="امتیاز",
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        default=3,
    )
    slug = models.SlugField(
        verbose_name="عبارت لینک", null=False, allow_unicode=True, max_length=200
    )

    def __str__(self):
        return self.title.title

    class Meta:
        verbose_name = "ویژگی‌ محصول"
        verbose_name_plural = "ویژگی‌های محصولات"
