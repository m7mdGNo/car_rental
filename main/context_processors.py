from .models import Car


def cars_count_to_base(request):
    cars_count = Car.objects.all()
    return {"cars_count": len(cars_count)}
