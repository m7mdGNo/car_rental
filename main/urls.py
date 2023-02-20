from django.urls import path
from .views import (
    HomeTemplateView,
    AboutTemplateView,
    CarsListView,
    BlogListView,
    SingleCarView,
    ReservationView,
    AddCarToCart,
    DeleteReservation,
    ContactUsView
)


urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("about/", AboutTemplateView.as_view(), name="about"),
    path("cars/", CarsListView.as_view(), name="cars"),
    path("blog/", BlogListView.as_view(), name="blog"),
    path("cars/<int:pk>/", SingleCarView.as_view(), name="single_car"),
    path('reservation/',ReservationView.as_view(),name='reservation_form'),
    path('add_to_cart/',AddCarToCart.as_view(),name='add_to_cart'),
    path('reservation/<int:id>/delete/',DeleteReservation,name='delete_reservation'),
    path('contactus/',ContactUsView.as_view(),name='contact_us')
]
