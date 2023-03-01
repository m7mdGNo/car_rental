from .models import Car
from django.db.models import Count


def cars_count_to_base(request):
    return {"cars_count": Car.objects.count()}
