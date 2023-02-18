from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class DeliveryDetailsForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(required=True, label="Phone")
    alt_phone = forms.CharField(required=False, label="Alternative Phone")
    country = forms.CharField(required=True, label="Country")
    state = forms.IntegerField(required=True, label="State")
    street = forms.IntegerField(required=True , label="Street")
    zone = forms.IntegerField(required=True, label="Zone")
    address = forms.IntegerField(required=True, label="Address")
    notes = forms.CharField(required=False, label="Notes")
    is_fast_delivery = forms.BooleanField(initial=False, required=False, label="Fast Delivary")

    class Meta:
        model = User
        fields = (
            "country",
            "alt_phone",
            "state",
            "street",
            "zone",
            "address",
            "notes",
            "is_fast_delivery",
            "first_name",
            "last_name",
            "email",
            "phone",
        )
