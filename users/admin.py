from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

# 3.5


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin @@ """

    fieldsets = UserAdmin.fieldsets + (  # 기존의 장고 form 이후로 추가
        (
            # 상단 파란 줄의 타이틀
            "Custom Profile",
            {
                # 파란 줄 아래의 요소들
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost"
                )
            }
        ),
    )

    list_filter = UserAdmin.list_filter + (
        "superhost",
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",

    )
# 3.4
# # admin.site.register(models.User, CustomUserAdmin)
# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):
#     # pass

#     """ Custom User Admin @@ """

#     list_display = ('username', 'email', 'gender','language', 'currency', 'superhost')
#     list_filter = ('language', 'currency', 'superhost',)
