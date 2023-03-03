from django.db.models import Q

import dcim.models
from netbox_reservations.models import Reservation


# Überschneidungen
# AStart vor BStart und AEnde nach BStart
# AStart vor BEnde und AEnde nach BEnde
# AStart nach BStart und AStart vor BEnde

def getConflictingReservations(instance):
    return Reservation.objects.filter(~Q(id=instance.id) &
                                      (
                                          (Q(start_date__lte=instance.start_date) & Q(
                                              end_date__gte=instance.start_date)) |
                                          (Q(start_date__lte=instance.end_date) & Q(end_date__gte=instance.end_date)) |
                                          (Q(start_date__gte=instance.start_date) & Q(
                                              start_date__lte=instance.end_date))
                                      )
                                      ).distinct()

