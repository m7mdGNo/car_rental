from django import forms
from .models import Reservation,ContactUs


        
class ReservationForm(forms.ModelForm):
    country = forms.CharField(max_length=100 ,required=True)
    city = forms.CharField(max_length=100 ,required=True)
    email = forms.CharField(max_length=100 ,required=True)
    pick_up_location = forms.CharField(max_length=100 ,required=True)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)

    class Meta:
        model = Reservation
        fields = (
            "country",
            "city",
            "email",
            "start_date",
            "end_date",
            "pick_up_location",
        )
        
        
        
class ContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=100 ,required=True)
    email = forms.CharField(max_length=100 ,required=True)
    subject = forms.CharField(max_length=100 ,required=True)
    message = forms.CharField(max_length=100 ,required=True)


    class Meta:
        model = ContactUs
        fields = (
            "name",
            "email",
            "subject",
            "message",

        )