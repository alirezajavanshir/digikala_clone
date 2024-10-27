from rest_framework import generics, permissions
from setting.models import SiteSetting, FAQCategory, FAQ
from .serializers import SiteSettingSerializer, FAQCategorySerializer, FAQSerializer


# ویو برای تنظیمات سایت
class SiteSettingListCreateView(generics.ListCreateAPIView):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SiteSettingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ویو برای دسته‌بندی سوالات
class FAQCategoryListCreateView(generics.ListCreateAPIView):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer


class FAQCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ویو برای سوالات متداول
class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class FAQRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
