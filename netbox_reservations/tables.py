import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, ColoredLabelColumn, columns
from .models import Reservation, Claim
from extras.models import Tag


class ReservationTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    contact = tables.Column(
        linkify=True
    )
    tenant = tables.Column(
        linkify=True
    )
    claim_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = Reservation
        fields = ('pk', 'id', 'name', 'claim_count', 'contact', 'tenant','start_date','end_date', 'comments')
        default_columns = ('name', 'contact', 'tenant', 'claim_count','start_date','end_date')


class ReducedClaimTable(NetBoxTable):
    tag = ColoredLabelColumn()
    restriction = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'tag', 'restriction', 'description',
        )
        default_columns = (
            'id', 'tag', 'restriction',
        )


class ClaimTable(NetBoxTable):
    reservation = tables.Column(
        linkify=True
    )
    tag = ColoredLabelColumn()
    restriction = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'reservation', 'tag', 'restriction', 'description',
        )
        default_columns = (
            'id','reservation', 'tag', 'restriction',
        )


class TagOverviewTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    color = columns.ColorColumn()
    claim_count = tables.Column()
    #lambda claim: claim.reservation.get_absolute_url()
    reservations = tables.Column(
        linkify=True
    )
    class Meta(NetBoxTable.Meta):
        model = Tag
        fields = ('pk', 'id','color', 'name', 'claim_count','reservations')
        default_columns = ('name', 'claim_count','reservations')
