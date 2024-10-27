from django.db import models
from django.utils.safestring import mark_safe
from product.models import Product
from extensions.utils import upload_image_path


class Images(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="gallery",
        verbose_name="محصول",
    )
    title = models.CharField(max_length=50, blank=True, verbose_name="عنوان")
    image = models.ImageField(
        upload_to=upload_image_path, blank=True, verbose_name="تصویر"
    )

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"

    def __str__(self):
        return self.title or "بدون عنوان"

    def image_tag(self):
        """Generate HTML for displaying the image."""
        return mark_safe(
            f'<img src="{self.image.url}" height="50" alt="{self.title}"/>'
        )

    image_tag.short_description = "تصویر"
