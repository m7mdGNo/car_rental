from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View, generic
from .forms import LoginForm, UserCreationForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.db.models import Prefetch
from main.models import Reservation, Car, Car_Brand, Brand_Model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


class LoginView(View):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                session_car_id_value = request.session.get("car_id", None)
                session_start_date = request.session.get("start_date", None)
                session_end_date = request.session.get("end_date", None)
                session_pick_up_location = request.session.get("pick_up_location", None)
                
                login(request, user)
                if session_car_id_value and session_start_date and session_end_date and session_pick_up_location:
                    car = Car.objects.get(id=session_car_id_value)
                    user.cart = car
                    user.cart_start_date = session_start_date
                    user.cart_end_date = session_end_date
                    user.cart_pick_up_location = session_pick_up_location
                    user.save()
                    return redirect("reservation_form")
                return redirect("home")
            else:
                form.add_error(None, "Invalid email or password")
        return render(request, self.template_name, {"form": form})


class SignUpView(generic.edit.CreateView):
    form_class = UserCreationForm
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save()
        request = self.request
        if user is not None:
            session_car_id_value = request.session.get("car_id", None)
            session_start_date = request.session.get("start_date", None)
            session_end_date = request.session.get("end_date", None)
            session_pick_up_location = request.session.get("pick_up_location", None)            
            login(request, user)
            if session_car_id_value and session_start_date and session_end_date and session_pick_up_location:
                car = Car.objects.get(id=session_car_id_value)
                user.cart = car
                user.cart_start_date = session_start_date
                user.cart_end_date = session_end_date
                user.cart_pick_up_location = session_pick_up_location
                user.save()
                return redirect("reservation_form")

            return redirect("home")

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profile.html"
    login_url = "/login/"

    def user_queryset(self):
        user = self.request.user
        qs = User.objects.prefetch_related(
            Prefetch(
                "reservations",
                Reservation.objects.prefetch_related(
                    Prefetch(
                        "car",
                        Car.objects.prefetch_related(
                            Prefetch(
                                "brand_model",
                                Brand_Model.objects.prefetch_related(
                                    Prefetch("brand", Car_Brand.objects.all())
                                ),
                            )
                        ),
                    )
                ),
            )
        ).get(id=user.id)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.user_queryset()

        ctx["user"] = user
        ctx["reservations"] = user.reservations.exclude(status="canceled")

        return ctx


@login_required(login_url="login")
def ProfileUpdate(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return HttpResponse(status=500)
    return HttpResponse(status=500)
