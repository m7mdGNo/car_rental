from django.urls import path
from .views import (
    LoginView,
    SignUpView,
    ProfileView,
    ProfileUpdate,
    CompanyProfileUpdate,
    CompanyRegistrationView,
    CompanyLoginView,
    CompanyProfileView,
    
)


urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('register/',SignUpView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdate,name='profile_update'),
    path('company/register/',CompanyRegistrationView.as_view(),name='company_register'),
    path('company/login/',CompanyLoginView.as_view(),name='company_login'),
    path('company/profile/',CompanyProfileView.as_view(),name='company_profile'),
    path('company/profile/update/',CompanyProfileUpdate,name='company_profile_update'),
]
