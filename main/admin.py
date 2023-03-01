from django.contrib import admin
from . import models
from .forms import ReservationForm

# Register your models here.


@admin.register(models.Car_Brand)
class Car_Brand_Admin(admin.ModelAdmin):
    """
    Admin class for the Car Brand model to be used in the Django Admin Panel
    """

    list_display = [
        "name",
    ]
    search_fields = ["name"]


class Brand_model_imgs_TabularInline(admin.TabularInline):
    """
    This TabularInline is used for displaying the 'img' field in the Brand Model admin page.
    """

    model = models.Brand_model_imgs
    fields = ["img"]


@admin.register(models.Brand_Model)
class Brand_model_Admin(admin.ModelAdmin):
    """
    Admin class for the Brand_model model to be used in the Django Admin Panel
    """

    list_display = ["name", "brand", "transmission", "year", "fuel"]
    list_filter = ["brand", "name", "transmission", "year", "fuel"]
    search_fields = ["name"]
    inlines = [Brand_model_imgs_TabularInline]

    # Method to get the brand name
    def brand(self, obj):
        return obj.brand.name


class Car_Review_TabularInline(admin.TabularInline):
    """
    This TabularInline is used for displaying the 'reviews' field in the car admin page.
    """

    model = models.CarReview
    fields = ["user", "car", "rate", "comment"]

    # Method to get the user who made the review
    def user(self, obj):
        return self.request.user


@admin.register(models.Car)
class Car_admin(admin.ModelAdmin):
    """
    Admin class for the Car model to be used in the Django Admin Panel
    """

    list_display = ["brand_model__name", "color", "company"]
    search_fields = ["brand_model__name", "color"]
    list_filter = [
        "company",
        "color",
        "brand_model__year",
    ]
    readonly_fields = ["rate"]

    # Method to get the brand model name
    def brand_model__name(self, obj):
        return obj.brand_model.name

    # Method to get the brand model year
    def brand_model__year(self, obj):
        return obj.brand_model.year

    inlines = [Car_Review_TabularInline]


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin class for the reservation model to be used in the Django Admin Panel
    """

    list_display = ["id", "email", "status", "start_date", "end_date", "created_at"]
    search_fields = ["id", "email"]
    list_filter = ["status", "country", "city", "created_at"]
    readonly_fields = ["total", "created_at"]


class BlogReviewTabularInline(admin.TabularInline):
    """
    This TabularInline is used for displaying the 'reviews' field in the blog admin page.
    """

    fields = ["user", "blog", "comment"]
    model = models.BlogReview


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Admin class for the Blog model to be used in the Django Admin Panel
    """

    list_display = ["title", "user", "created_at"]
    list_filter = ["user", "created_at"]
    search_fields = ["title", "user"]

    inlines = [BlogReviewTabularInline]


admin.site.register(models.ContactUs)
