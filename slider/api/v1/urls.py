from django.urls import path
from .views import SliderListCreateView, SliderRetrieveUpdateDestroyView

urlpatterns = [
    # URL برای لیست و ایجاد اسلایدها
    path("sliders/", SliderListCreateView.as_view(), name="slider-list-create"),
    # URL برای دریافت، به‌روزرسانی و حذف اسلایدها
    path(
        "sliders/<int:pk>/",
        SliderRetrieveUpdateDestroyView.as_view(),
        name="slider-retrieve-update-destroy",
    ),
]
