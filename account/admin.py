from django.contrib import admin
from .models import UserProfile, UserAddress, History


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone",
        "national_code",
        "image_tag",
    ]


class UserAddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone",
        "ostan",
        "city",
        "selected",
    ]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(History)
