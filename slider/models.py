from django.db import models
from extensions.utils import upload_image_path

# برای آپلود عکس و درست کردن آدرسش


# Create your models here.
class Slider(models.Model):
    title = models.CharField("عنوان", max_length=150)
    link = models.URLField("لینک", max_length=150)
    description = models.TextField("توضیحات")
    image = models.ImageField(
        "تصویر", upload_to=upload_image_path, null=True, blank=True
    )

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرها"

    def __str__(self):
        return self.title
