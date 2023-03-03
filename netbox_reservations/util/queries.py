from django.db.models import Q

from netbox_reservations.models import Reservation


def getConflictingReservations(instance):
    return Reservation.objects.filter(
        Q(end_date__lte=instance.end_date) & Q(end_date__gte=instance.end_date) & ~Q(id=instance.id)
    ).distinct()
