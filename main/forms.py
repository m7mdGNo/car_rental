from django import forms
from .models import Reservation,ContactUs,Car


        
class ReservationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100 ,required=True)
    last_name = forms.CharField(max_length=100 ,required=True)
    phone_number = forms.CharField(max_length=100 ,required=True)
    country = forms.CharField(max_length=100 ,required=True)
    address = forms.CharField(max_length=100 ,required=True)
    postcode = forms.CharField(max_length=100 ,required=True)
    city = forms.CharField(max_length=100 ,required=True)
    email = forms.CharField(max_length=100 ,required=True)


    class Meta:
        model = Reservation
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "address",
            "postcode",
            "city",
            "email",
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
        
        
        
class CarsForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand_model',
            'plate_number',
            'description',
            'mileage',
            'color',
            'price',
            'image',
        ]