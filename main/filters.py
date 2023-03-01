import django_filters
from .models import Car, Reservation
from django.utils import timezone
from django.db.models import Q


class AvailableCarsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        method="filter_by_start_date",
    )
    end_date = django_filters.DateFilter(
        method="filter_by_end_date",
    )

    def filter_by_start_date(self, queryset, name, value):
        start_datetime = value
        return queryset.exclude(
            reservation_cars__reservation__start_date__lt=start_datetime,
            reservation_cars__reservation__end_date__gt=start_datetime,
        )

    def filter_by_end_date(self, queryset, name, value):
        end_datetime = value

        return queryset.exclude(
            reservation_cars__reservation__start_date__lt=end_datetime,
            reservation_cars__reservation__end_date__gt=end_datetime,
        )
