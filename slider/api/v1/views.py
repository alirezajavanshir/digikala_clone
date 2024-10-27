from rest_framework import generics, permissions
from slider.models import Slider
from .serializers import SliderSerializer


# ویو برای لیست و ایجاد اسلایدها
class SliderListCreateView(generics.ListCreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ویو برای دریافت، به‌روزرسانی و حذف اسلایدها
class SliderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
