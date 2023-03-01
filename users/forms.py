from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User, Company


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

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
    """
    A form for edit user informations.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "image",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class LoginForm(forms.Form):
    """
    A form for login.
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "image",
        )


class CompanyForm(forms.ModelForm):
    """
    A form for add company with validations and cleans.
    """

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = Company
        fields = ["name", "country", "governate", "city", "place", "website", "about"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Company.objects.filter(name=name).exists():
            raise forms.ValidationError("A company with that name already exists.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        company = super().save(commit=False)
        user = User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )
        company.user = user
        if commit:
            company.save()
        return company


class CompanyLoginForm(forms.Form):
    """
    A form for company login in website.
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.get(email=email)
        if user:
            if Company.objects.filter(user=user).exists():
                return email
            raise forms.ValidationError("This email isn't Company Email.")


class CompanyUpdateForm(forms.ModelForm):
    """
    A form for update company data
    """

    class Meta:
        model = Company
        fields = (
            "name",
            "website",
            "country",
            "governate",
            "city",
            "place",
            "about",
            "image",
        )
