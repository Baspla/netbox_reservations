from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import ReservationSerializer, ClaimSerializer


class ReservationViewSet(NetBoxModelViewSet):
    queryset = models.Reservation.objects.prefetch_related('tags', 'tenant', 'contact').annotate(
        claim_count=Count('claims')
    )
    serializer_class = ReservationSerializer


class ClaimViewSet(NetBoxModelViewSet):
    queryset = models.Claim.objects.prefetch_related(
        'reservation', 'tag'
    )
    serializer_class = ClaimSerializer
    #filterset_class = filtersets.ClaimFilterSet

