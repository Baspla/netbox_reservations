from netbox.filtersets import NetBoxModelFilterSet
from .models import Claim, Reservation


class ClaimFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Claim
        fields = ('id', 'reservation', 'tag', 'restriction')

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)

class ReservationFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Reservation
        fields = ('id', 'name', 'contact', 'tenant', 'start_date', 'end_date','claims')

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
