from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View, generic
from .forms import LoginForm, UserCreationForm,UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.db.models import Prefetch
from main.models import Reservation, ReservationItem, Car, Car_Brand, Brand_Model
from django.contrib.auth.decorators import login_required



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
                login(request, user)
                if session_car_id_value:
                    user.cart.add(session_car_id_value)
                    user.save()
                    del request.session["car_id"]
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
            login(request, user)
            if session_car_id_value:
                user.cart.add(session_car_id_value)
                user.save()
                del request.session["car_id"]
                return redirect("reservation_form")

            return redirect("home")

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profile.html"
    login_url = "/login/"

    def user_queryset(self):
        user = self.request.user
        qs = User.objects.filter(id=user.id).prefetch_related(
            Prefetch(
                "reservations",
                Reservation.objects.prefetch_related(
                    Prefetch(
                        "items",
                        ReservationItem.objects.prefetch_related(
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
                ),
            )
        )
        return qs.get()
    
        

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.user_queryset()
        
        ctx['user'] = user
        ctx['reservations'] = user.reservations.exclude(status='canceled')
        
        return ctx


@login_required('login')
def ProfileUpdate(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')