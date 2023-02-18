from django.shortcuts import render
from django.views import View, generic
from .models import Car, Brand_Model, Car_Brand, Blog,Reservation,ReservationItem
from django.db.models import Q, F, Sum, Avg, Count, Max, Prefetch
from django.core.paginator import Paginator
from .filters import AvailableCarsFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ReservationForm


# Create your views here.
class HomeTemplateView(generic.TemplateView):
    template_name = "index.html"
    car_queryset = (
        Car.objects.all()
        .prefetch_related(
            Prefetch("brand_model", Brand_Model.objects.prefetch_related("brand"))
        )
        .prefetch_related("images")
    ).filter(accepted=True)

    blog_queryset = (
        Blog.objects.all()
        .prefetch_related("user")
        .annotate(reviews_count=Count("reviews"))
    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featuerd_cars"] = self.car_queryset[:8]
        ctx["blogs"] = self.blog_queryset[:3]
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

    paginate_by = 12

    context_object_name = "featuerd_cars"

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
    paginate_by = 4

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
        reservation = form.save()
        car = user.cart.first()
        item = ReservationItem(reservation=reservation, car=car,price=car.price)
        item.save()
        user.cart.clear()
        user.save()
        return super().form_valid(form)


class LoginView(generic.TemplateView):
    template_name = 'login.html'
    
    
    
    
class AddCarToCart(View):
    def post(self, request, *args, **kwargs):
        car_id = int(request.POST.get('car_id'))
        user = request.user

        if user.is_authenticated:
            user.cart.clear()
            user.cart.add(car_id)
            user.save()
            return JsonResponse({'success':True})
        
        request.session['car_id'] = car_id
        request.session.modified=True
        
        return JsonResponse({'success':True})
         
        
    