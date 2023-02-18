from django import forms
from .models import Reservation


        
class ReservationForm(forms.ModelForm):
    country = forms.CharField(max_length=100 ,required=True)
    city = forms.CharField(max_length=100 ,required=True)
    email = forms.CharField(max_length=100 ,required=True)
    pick_up_location = forms.CharField(max_length=100 ,required=True)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    payment_method = forms.ChoiceField(choices=Reservation.PaymentChoices.choices,required=True)

    class Meta:
        model = Reservation
        fields = (
            "country",
            "city",
            "email",
            "start_date",
            "end_date",
            "pick_up_location",
            "payment_method",
        )