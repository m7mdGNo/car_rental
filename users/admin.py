from django.contrib import admin
from .forms import UserCreationForm, UserEditForm
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _




class CustomUserAdmin(UserAdmin):
    form = UserEditForm
    add_form = UserCreationForm
    ordering = (
        "-created_at",
        "email",
    )
    search_fields = ("first_name", "last_name", "email")
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name","image")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at")}),
        (_("cart car"), {"fields": ("cart", "cart_start_date","cart_end_date","cart_pick_up_location")}),
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


admin.site.register(User, CustomUserAdmin)
