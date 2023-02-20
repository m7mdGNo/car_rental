from django.urls import path
from .views import (
    LoginView,
    SignUpView,
    ProfileView,
    ProfileUpdate,
)


urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('register/',SignUpView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdate,name='profile_update')
]
