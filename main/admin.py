from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Car_Brand)
class Car_Brand_Admin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = ["name"]


class Brand_model_imgs_TabularInline(admin.TabularInline):
    model = models.Brand_model_imgs
    fields = ["img"]


@admin.register(models.Brand_Model)
class Brand_model_Admin(admin.ModelAdmin):
    list_display = ["name", "brand", "transmission", "color", "year", "fuel"]
    list_filter = ["brand", "name", "transmission", "color", "year", "fuel"]
    search_fields = ["name"]
    inlines = [Brand_model_imgs_TabularInline]

    def brand(self, obj):
        return obj.brand.name


class Car_imgs_TabularInline(admin.TabularInline):
    model = models.Car_imgs
    fields = ["img"]


@admin.register(models.Car)
class Car_admin(admin.ModelAdmin):
    list_display = ["brand_model__name", "owner"]
    search_fields = ["brand_model__name"]
    list_filter = [
        "owner",
        "brand_model__name",
        "brand_model__year",
        "brand_model__color",
    ]

    def brand_model__name(self, obj):
        queryset = models.Brand_Model.objects.filter(id=obj.id).get()
        return queryset.name

    def brand_model__year(self, obj):
        queryset = models.Brand_Model.objects.filter(id=obj.id).get()
        return queryset.year

    def brand_model__color(self, obj):
        queryset = models.Brand_Model.objects.filter(id=obj.id).get()
        return queryset.color

    inlines = [Car_imgs_TabularInline]


class ReservationItem_TabularInline(admin.TabularInline):
    model = models.ReservationItem
    fields = ["reservation", "car", "price"]


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "status", "start_date", "end_date"]
    search_fields = ["id", "email"]
    list_filter = ["status", "country", "city", "created"]
    readonly_fields = ['total',]

    inlines = [ReservationItem_TabularInline]


class BlogReviewTabularInline(admin.TabularInline):
    fields = ["user", "blog", "comment"]
    model = models.BlogReview


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_at"]
    list_filter = ["user", "created_at"]
    search_fields = ["title", "user"]

    inlines = [BlogReviewTabularInline]


admin.site.register(models.ContactUs)