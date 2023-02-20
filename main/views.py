from django.shortcuts import render,redirect
from django.views import View, generic
from .models import Car, Brand_Model, Car_Brand, Blog,Reservation,ReservationItem,ContactUs
from django.db.models import Q, F, Sum, Avg, Count, Max, Prefetch
from django.core.paginator import Paginator
from .filters import AvailableCarsFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm,ContactUsForm
from django.urls import reverse


# Create your views here.
class HomeTemplateView(generic.TemplateView):
    template_name = "index.html"
    
    def get_car_queryset(self):
        return (
            Car.objects.all()
            .prefetch_related(
                Prefetch("brand_model", Brand_Model.objects.prefetch_related("brand"))
            )
            .prefetch_related("images")
            .filter(accepted=True)[:8]
        )

    def get_blog_queryset(self):
        return (
            Blog.objects.all()
            .prefetch_related("user")
            .annotate(reviews_count=Count("reviews"))
            .order_by("-id")[:3]
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featuerd_cars"] = self.get_car_queryset()
        ctx["blogs"] = self.get_blog_queryset()
        return ctx



class CarsListView(generic.ListView):
    template_name = "car.html"

    queryset = (
        Car.objects.prefetch_related(
            Prefetch("brand_model", Brand_Model.objects.prefetch_related("brand"))
        )
        .prefetch_related("images")
        .order_by("added_at")
    ).filter(accepted=True)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 12)

    context_object_name = "featured_cars"

    filter_class = AvailableCarsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=queryset)
        return self.filter.qs


class BlogListView(generic.ListView):
    template_name = "blog.html"
    queryset = Blog.objects.prefetch_related("user").annotate(
        reviews_count=Count("reviews")
    )
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 4)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["blogs"] = ctx["object_list"]
        return ctx


class SingleCarView(generic.DetailView):
    template_name = "car-single.html"
    queryset = (
        Car.objects.prefetch_related(
            Prefetch("brand_model", Brand_Model.objects.prefetch_related("brand"))
        ).prefetch_related("images")
    ).filter(accepted=True)

    context_object_name = "car"


class AboutTemplateView(generic.TemplateView):
    template_name = "about.html"


class ReservationView(LoginRequiredMixin,generic.CreateView):
    template_name = 'reservation_form.html'
    login_url = '/login/'
    
    model = Reservation
    form_class = ReservationForm

    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        self.reservation = form.save()
        car = user.cart.last()
        item = ReservationItem(reservation=self.reservation, car=car,price=car.price)
        item.save()
        # return super().form_valid(form)
        return redirect(reverse('checkout', kwargs={'reservation_id': self.reservation.id}))


    
    
class AddCarToCart(View):
    def post(self, request, *args, **kwargs):
        car_id = int(request.POST.get('car_id'))
        user = request.user

        if user.is_authenticated:
            user.cart.clear()
            user.cart.add(car_id)
            user.save()
            return redirect('reservation_form')
        
        request.session['car_id'] = car_id
        request.session.modified=True
        
        return redirect("reservation_form")
            
        
    
def DeleteReservation(request,id):
    if request.method == 'GET':
        reservation = Reservation.objects.filter(id=id).get()
        if reservation.status == "paid":
            reservation.status = "pernding_refund"
            reservation.save()
    return redirect('profile')




class ContactUsView(generic.CreateView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    model = ContactUs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        value = self.request.session.get('contact_us',False)
        context["success"] = value
        if value:
            del self.request.session['contact_us']
        return context
    
    def form_valid(self, form):
        self.contact_us = form.save()
        self.request.session['contact_us'] = True
        return redirect('contact_us')