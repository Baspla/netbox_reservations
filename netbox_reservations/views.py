import re
from itertools import chain
from logging import warning

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Subquery, OuterRef, Exists, Q, When, Case, Value
from django.utils import timezone
from django.views.generic import TemplateView
from tree_queries.query import TreeQuerySet

from dcim.models import Device
from netbox.views import generic
from extras.models import Tag
from . import filtersets, forms, models, tables
from .models import Reservation, ClaimQuerySet
from .tables import ReservationTable
from .util.queries import getConflictingReservations


#
# Reservation views
#

class ReservationView(generic.ObjectView):
    queryset = models.Reservation.objects.all()

    permission_required = "netbox_reservations.view_reservation"

    def get_extra_context(self, request, instance):
        table = tables.ReducedClaimTable(ClaimQuerySet(model=models.Claim).with_tree_fields()
                                         .filter(reservation=instance))
        table.configure(request)

        conflict_reservations = getConflictingReservations(instance)
        conflict_table = ReservationTable(conflict_reservations)

        return {
            'claims_table': table,
            'conflict_table': conflict_table,
        }


class ReservationListView(generic.ObjectListView):
    queryset = models.Reservation.objects.annotate(
        claim_count=Count('claims')
    )
    table = tables.ReservationTable
    filterset = filtersets.ReservationFilterSet
    filterset_form = forms.ReservationFilterForm

    permission_required = "netbox_reservations.view_reservation"


class ReservationEditView(generic.ObjectEditView):
    queryset = models.Reservation.objects.all()
    form = forms.ReservationForm

    permission_required = "netbox_reservations.edit_reservation"


class ReservationDeleteView(generic.ObjectDeleteView):
    queryset = models.Reservation.objects.all()

    permission_required = "netbox_reservations.delete_reservation"

    #
    # Claim views
    #


class ClaimView(generic.ObjectView):
    queryset = models.Claim.objects.all()

    permission_required = "netbox_reservations.view_claim"


# This pattern is used to check if the filter is acceptable
# This means that indentation will only be used if the filter matches this regex or "(AND: )" which is the default.
pattern = re.compile(
    "^\(AND: RelatedExact\(Col\(netbox_reservations_claim, netbox_reservations.Claim.reservation\), \d+\)\)$")


class ClaimListView(generic.ObjectListView):
    queryset = ClaimQuerySet(model=models.Claim).with_tree_fields()
    table = tables.ClaimTable
    filterset = filtersets.ClaimFilterSet
    filterset_form = forms.ClaimFilterForm

    def get_extra_context(self, request):
        return {
            'has_filter': bool(request.GET),
            'filter': str(self.queryset.has_filters()),
            'has_acceptable_filter': bool(pattern.fullmatch(str(self.queryset.has_filters()))),
        }

    permission_required = "netbox_reservations.view_claim"


class ClaimEditView(generic.ObjectEditView):
    queryset = models.Claim.objects.all()
    form = forms.ClaimForm

    permission_required = "netbox_reservations.edit_claim"


class ClaimDeleteView(generic.ObjectDeleteView):
    queryset = models.Claim.objects.all()

    permission_required = "netbox_reservations.delete_claim"


#
# Tag overview
#


class TagOverviewListView(generic.ObjectListView):
    queryset = Tag.objects \
        .annotate(reservation_count=Count('claims', filter=Q(claims__reservation__start_date__lte=timezone.now(),
                                                             claims__reservation__end_date__gte=timezone.now(),
                                                             claims__reservation__is_draft=False)))
    table = tables.TagOverviewTable

    permission_required = "netbox_reservations.view_claim"
