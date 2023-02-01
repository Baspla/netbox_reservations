import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, ColoredLabelColumn
from .models import Reservation, Claim


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
