from django.shortcuts import render, redirect
from django.views import View, generic
from .models import Car, Brand_Model, Car_Brand, Blog, Reservation, ContactUs
from django.db.models import Q, F, Sum, Avg, Count, Max, Prefetch
from django.core.paginator import Paginator
from .filters import AvailableCarsFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm, ContactUsForm, CarsForm
from django.urls import reverse
import stripe
from users.models import Company
from .mixins import CompanyRequiredMixin


# Create your views here.
class HomeTemplateView(generic.TemplateView):
    template_name = "index.html"

    def get_blog_queryset(self):
        return (
            Blog.objects.all()
            .prefetch_related("user")
            .annotate(reviews_count=Count("reviews"))
            .order_by("-id")[:3]
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["blogs"] = self.get_blog_queryset()
        return ctx


class CarsListView(generic.ListView):
    template_name = "car.html"

    queryset = (
        Car.objects.prefetch_related(
            Prefetch("brand_model", Brand_Model.objects.prefetch_related("brand"))
        ).order_by("added_at")
    ).filter(accepted=True)

    # def get_paginate_by(self, queryset):
    #     return self.request.GET.get("paginate_by", 12)

    context_object_name = "featured_cars"

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date and end_date:
            reserved_cars = Reservation.objects.filter(
                Q(start_date__lte=start_date, end_date__gte=end_date)
                | Q(start_date__lte=start_date, end_date__gte=start_date)
                | Q(start_date__lte=end_date, end_date__gte=end_date)
                | Q(start_date__gte=start_date, end_date__lte=end_date)
            ).values_list("car__id", flat=True)
            queryset = queryset.exclude(id__in=reserved_cars)
            return queryset
        else:
            return []


class BlogListView(generic.ListView):
    template_name = "blog.html"
    queryset = Blog.objects.prefetch_related("user").annotate(
        reviews_count=Count("reviews")
    )

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", 4)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["blogs"] = ctx["object_list"]
        return ctx


class BlogSingleView(generic.TemplateView):
    template_name = 'blog-single.html'

class SingleCarView(generic.DetailView):
    template_name = "car-single.html"
    queryset = (
        Car.objects.prefetch_related(
            Prefetch("brand_model", Brand_Model.objects.prefetch_related("brand"))
        )
        .prefetch_related("reviews")
        .filter(accepted=True)
    )

    context_object_name = "car"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["reviews_counter"] = self.get_object().reviews.aggregate(Count("rate"))[
            "rate__count"
        ]
        return ctx


class CarDeleteView(CompanyRequiredMixin,generic.DeleteView):
    model = Car

    def get_success_url(self):
        return reverse("company_profile")

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CarUpdateView(CompanyRequiredMixin,generic.UpdateView):
    model = Car
    form_class = CarsForm
    template_name = "update_car.html"
    context_object_name = "car"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['brand_models'] = Brand_Model.objects.all()
        return ctx

    def get_success_url(self):
        return reverse("company_profile")

    def form_valid(self, form):
        form.instance.company = Company.objects.get(user=self.request.user)
        return super().form_valid(form)


class CarCreateView(CompanyRequiredMixin,generic.CreateView):
    model = Car
    form_class = CarsForm
    template_name = "add_car.html"
    context_object_name = "car"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['brand_models'] = Brand_Model.objects.all()
        return ctx

    def get_success_url(self):
        return reverse("company_profile")

    def form_valid(self, form):
        form.instance.company = Company.objects.get(user=self.request.user)
        return super().form_valid(form)


class AboutTemplateView(generic.TemplateView):
    template_name = "about.html"


class ReservationView(LoginRequiredMixin, generic.CreateView):
    template_name = "reservation_form.html"
    login_url = "/login/"

    model = Reservation
    form_class = ReservationForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.car = user.cart
        form.instance.start_date = user.cart_start_date
        form.instance.end_date = user.cart_end_date
        form.instance.pick_up_location = user.cart_pick_up_location
        self.reservation = form.save()
        return redirect(
            reverse("checkout", kwargs={"reservation_id": self.reservation.id})
        )


class AddCarToCart(View):
    def post(self, request, *args, **kwargs):
        car_id = int(request.POST.get("car_id"))
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        pick_up_location = request.POST.get("pick_up_location")
        car = Car.objects.get(id=car_id)
        user = request.user

        if user.is_authenticated:
            user.cart = car
            user.cart_start_date = start_date
            user.cart_end_date = end_date
            user.cart_pick_up_location = pick_up_location
            user.save()
            return redirect("reservation_form")

        request.session["car_id"] = car_id
        request.session["start_date"] = start_date
        request.session["end_date"] = end_date
        request.session["pick_up_location"] = pick_up_location
        request.session.modified = True

        print("added")
        return redirect("reservation_form")


def DeleteReservation(request, id):
    if request.method == "GET":
        reservation = Reservation.objects.get(id=id)
        if reservation.status == "paid":
            reservation.status = "pernding_refund"
            reservation.save()
    return redirect("profile")


class ContactUsView(generic.CreateView):
    template_name = "contact.html"
    form_class = ContactUsForm
    model = ContactUs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        value = self.request.session.get("contact_us", False)
        context["success"] = value
        if value:
            del self.request.session["contact_us"]
        return context

    def form_valid(self, form):
        self.contact_us = form.save()
        self.request.session["contact_us"] = True
        return redirect("contact_us")
