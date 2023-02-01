from netbox.filtersets import NetBoxModelFilterSet
from .models import Claim, Reservation
from django_filters import DateFilter
import logging

logger = logging.getLogger('netbox.reservations')


class ClaimFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Claim
        fields = ('id', 'reservation', 'tag', 'restriction')

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)

class ReservationFilterSet(NetBoxModelFilterSet):
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    class Meta:
        model = Reservation
        fields = ('id', 'name', 'contact', 'tenant','start_date', 'end_date','claims')


    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
