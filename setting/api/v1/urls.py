from django.urls import path
from .views import (
    SiteSettingListCreateView,
    SiteSettingRetrieveUpdateDestroyView,
    FAQCategoryListCreateView,
    FAQCategoryRetrieveUpdateDestroyView,
    FAQListCreateView,
    FAQRetrieveUpdateDestroyView,
)

urlpatterns = [
    # URL برای تنظیمات سایت
    path(
        "site-settings/",
        SiteSettingListCreateView.as_view(),
        name="site-settings-list-create",
    ),
    path(
        "site-settings/<int:pk>/",
        SiteSettingRetrieveUpdateDestroyView.as_view(),
        name="site-settings-retrieve-update-destroy",
    ),
    # URL برای دسته‌بندی سوالات
    path(
        "faq-categories/",
        FAQCategoryListCreateView.as_view(),
        name="faq-categories-list-create",
    ),
    path(
        "faq-categories/<int:pk>/",
        FAQCategoryRetrieveUpdateDestroyView.as_view(),
        name="faq-categories-retrieve-update-destroy",
    ),
    # URL برای سوالات متداول
    path("faqs/", FAQListCreateView.as_view(), name="faqs-list-create"),
    path(
        "faqs/<int:pk>/",
        FAQRetrieveUpdateDestroyView.as_view(),
        name="faqs-retrieve-update-destroy",
    ),
]
