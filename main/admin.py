from django.contrib import admin
from . import models
from .forms import ReservationForm
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
    list_display = ["name", "brand", "transmission", "year", "fuel"]
    list_filter = ["brand", "name", "transmission", "year", "fuel"]
    search_fields = ["name"]
    inlines = [Brand_model_imgs_TabularInline]

    def brand(self, obj):
        return obj.brand.name


class Car_Review_TabularInline(admin.TabularInline):
    model = models.CarReview
    fields = ['user','car','rate','comment']
    
    def user(self,obj):
        return self.request.user


@admin.register(models.Car)
class Car_admin(admin.ModelAdmin):
    list_display = ["brand_model__name", "color", "company"]
    search_fields = ["brand_model__name", "color"]
    list_filter = [
        "company",
        "color",
        "brand_model__year",
    ]
    readonly_fields = ['rate']

    def brand_model__name(self, obj):
        return obj.brand_model.name

    def brand_model__year(self, obj):
        return obj.brand_model.year

    inlines = [Car_Review_TabularInline]


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "status", "start_date", "end_date","created_at"]
    search_fields = ["id", "email"]
    list_filter = ["status", "country", "city","created_at"]
    readonly_fields = [
        "total",
        "created_at"
    ]


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
