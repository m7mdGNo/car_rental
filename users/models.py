from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from main.models import Car


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    temp_password = models.CharField(max_length=100, null=True, blank=True)
    
    image = models.ImageField(default='profile.png')

    cart = models.ManyToManyField(
        Car, through="CartItem", blank=True, related_name="cart"
    )

    start_date = models.DateTimeField(auto_now_add=True)
    about = models.TextField(_("about"), max_length=500, blank=True)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_superuser = models.BooleanField(
        "Superuser status",
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )

    is_owner = models.BooleanField(
        "owner status",
        default=False,
        help_text="Designates that this user is a car owner.",
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def username(self):
        return self.email

    def get_username(self):
        return self.email

    def __str__(self):
        return self.email


class BillingAddress(models.Model):
    user = models.ForeignKey(
        User, related_name="billing_adresses", on_delete=models.CASCADE
    )
    email = models.EmailField()
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cart_items')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "car"]
