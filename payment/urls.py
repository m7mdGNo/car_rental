from django.urls import path
from .views import checkout, stripe_webhook

urlpatterns = [
    path("checkout/<int:reservation_id>", checkout, name="checkout"),
    path("webhooks/stripe/", stripe_webhook, name="stripe-webhook"),
]
