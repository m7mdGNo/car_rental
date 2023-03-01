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
    ContactUsView,
    CarDeleteView,
    CarUpdateView,
    CarCreateView,
    BlogSingleView
)


urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("about/", AboutTemplateView.as_view(), name="about"),
    
    path("cars/", CarsListView.as_view(), name="cars"),
    path("car/<int:pk>/", SingleCarView.as_view(), name="single_car"),
    path('car/delete/<int:pk>/',CarDeleteView.as_view(),name='delete_car'),
    path('car/udpate/<int:pk>/',CarUpdateView.as_view(),name='update_car'),
    path('car/add/',CarCreateView.as_view(),name='add_car'),
    
    path("blog/", BlogListView.as_view(), name="blog"),
    path('blog/<int:pk>/',BlogSingleView.as_view(),name='blog_single'),
    
    path('reservation/',ReservationView.as_view(),name='reservation_form'),
    path('reservation/<int:id>/delete/',DeleteReservation,name='delete_reservation'),
    path('add_to_cart/',AddCarToCart.as_view(),name='add_to_cart'),
    
    path('contactus/',ContactUsView.as_view(),name='contact_us'),
    
]
