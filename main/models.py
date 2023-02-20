from django.db import models
from django.db.models import Sum, Count, F
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Car_Brand(models.Model):
    name = models.CharField(max_length=150)
    img = models.ImageField(default="placeholder.png")

    def __str__(self) -> str:
        return self.name


class Brand_Model(models.Model):
    brand = models.ForeignKey(
        Car_Brand, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=150)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=150)

    class TransmissionChoices(models.TextChoices):
        MANUAL = "manual", "Manual"
        AUTOMATIC = "automatic", "Automatic"

    transmission = models.CharField(
        max_length=150,
        choices=TransmissionChoices.choices,
        default=TransmissionChoices.MANUAL,
    )

    class FuelChoices(models.TextChoices):
        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        Natural_Gas = "natural gas", "Natural Gas"
        ELECTRIC = "electric", "Electric"

    fuel = models.CharField(
        max_length=150,
        choices=FuelChoices.choices,
        default=FuelChoices.PETROL,
    )
    seats = models.IntegerField()
    luggage = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Brand_model_imgs(models.Model):
    brand_model = models.ForeignKey(
        Brand_Model, on_delete=models.CASCADE, related_name="imgs"
    )
    img = models.ImageField(default="placeholder.png")


class Car(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    brand_model = models.ForeignKey(Brand_Model, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=12)
    description = models.TextField(max_length=1000)
    mileage = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("single_car", args=[self.id])

    def __str__(self) -> str:
        return f"{self.brand_model.brand.name}|{self.brand_model.name}"


class Car_imgs(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    img = models.ImageField(default="placeholder.png")


class Reservation(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE,related_name='reservations')
    country = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    pick_up_location = models.CharField(max_length=100)

    class StatusChoices(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELED = "canceled", "Canceled"
        PENDING_REFUND = "pernding_refund", "Pending refund"
        REFUNDED = "refunded", "Refunded"
        DELIVERED = "delivered", "Delivered"

    status = models.CharField(
        max_length=150, choices=StatusChoices.choices, default=StatusChoices.UNPAID
    )

    class Meta:
        ordering = ["-created"]

    @property
    def count(self):
        return self.items.aggregate(count=Sum("quantity"))

    @property
    def total(self):
        days = (self.end_date - self.start_date).days
        price = self.items.first().car.price
        return days*price

    def __str__(self):
        return f"Reservation {self.id}"


class ReservationItem(models.Model):
    reservation = models.ForeignKey(
        Reservation, related_name="items", on_delete=models.CASCADE
    )
    car = models.ForeignKey(
        Car, related_name="reservation_cars", on_delete=models.CASCADE
    )
    price = models.FloatField()

    def __str__(self):
        return str(self.id)


class CarReview(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(
        validators=[MaxValueValidator(5, "Can't rate car with more than 5 starts")]
    )
    comment = models.TextField()

    class Meta:
        unique_together = ["user", "car"]


class Blog(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    describtion = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.title

    # def get_absolute_url(self):
    #     return reverse("model_detail", args=[self.id,])


class BlogReview(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()

    class Meta:
        unique_together = ["user", "blog"]




class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    
    def __str__(self) -> str:
        return self.name