from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from main.models import (
    Reservation,
    Car,
    ReservationItem,
    Car_imgs,
    Brand_Model,
    Car_Brand,
)
from django.db.models import Prefetch
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required



stripe_pub_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY
stripe.api_key = stripe_secret_key


def checkout(request, reservation_id):
    reservation = (
        Reservation.objects.filter(id=reservation_id)
        .prefetch_related(
            Prefetch(
                "items",
                ReservationItem.objects.prefetch_related(
                    Prefetch(
                        "car",
                        Car.objects.prefetch_related(
                            Prefetch(
                                "brand_model",
                                Brand_Model.objects.prefetch_related(
                                    Prefetch("brand", Car_Brand.objects.all())
                                ),
                            )
                        ).prefetch_related("images"),
                    )
                ),
            )
        )
        .get()
    )

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{reservation.items.first().car.brand_model.brand.name} {reservation.items.first().car.brand_model.name} {reservation.items.first().car.brand_model.year}",
                    },
                    "unit_amount": reservation.total*100,
                },
                "quantity": 1,
            }
        ],
        metadata={
                "reservation_id": reservation.id
            },
        mode="payment",
        success_url=f"{settings.DOMAIN}/",
        cancel_url=f"{settings.DOMAIN}/reservation",
    )
    return redirect(checkout_session.url, code=303)



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        user = request.user
        session = event.data.object
        reservation_id = session.metadata['reservation_id']
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.status = 'paid'
        reservation.save()
        user.cart.clear()
        user.save()


    return HttpResponse(status=200)