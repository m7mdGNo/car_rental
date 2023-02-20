from django.contrib import admin
from .forms import UserCreationForm, UserEditForm
from .models import User, CartItem
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    extra: int = 0
    readonly_fields = ("price",)

    def price(self, obj):
        return obj.car.price


class CustomUserAdmin(UserAdmin):
    form = UserEditForm
    add_form = UserCreationForm
    ordering = (
        "-start_date",
        "email",
    )
    search_fields = ("first_name", "last_name", "email")
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    readonly_fields = ("start_date",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name","image")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "start_date")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = [CartItemAdmin]


admin.site.register(User, CustomUserAdmin)
