from django.db.models import Q

from extras.models import Tag
from netbox.filtersets import NetBoxModelFilterSet
from .models import Claim, Reservation
from django_filters import DateTimeFilter, ModelMultipleChoiceFilter


class ClaimFilterSet(NetBoxModelFilterSet):
    tag = ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    class Meta:
        model = Claim
        fields = ('id', 'reservation', 'tag', 'restriction')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(description__icontains=value) |
            Q(reservation__name__icontains=value) |
            Q(reservation__contact__name__icontains=value) |
            Q(reservation__tenant__name__icontains=value) |
            Q(tags__name__icontains=value)
        )
        return queryset.filter(qs_filter)


class ReservationFilterSet(NetBoxModelFilterSet):
    start_date = DateTimeFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateTimeFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Reservation
        fields = ('id', 'name', 'contact', 'tenant', 'start_date', 'end_date', 'claims')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(comments__icontains=value) |
            Q(name__icontains=value) |
            Q(contact__name__icontains=value) |
            Q(tenant__name__icontains=value)
        )
        return queryset.filter(qs_filter)
