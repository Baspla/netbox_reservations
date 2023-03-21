import django_tables2 as tables

from dcim.models import Device
from netbox.tables import NetBoxTable, ChoiceFieldColumn, ColoredLabelColumn, columns
from .models import Reservation, Claim
from extras.models import Tag


class CustomColoredMPTTColumn(tables.TemplateColumn):
    """
        Display a nested hierarchy for MPTT-enabled models.
        has_filter is set if any GET Parameters are sent.
        If this fails at any point you could test if filter is equal to (AND: ) or you can use the has_filter variable.
        has_filter and filter are provided as additional context variables by views.py
        """
    template_code = """
            {% load helpers %}
            <!-- filter used: {{ filter }} -->
            {% if filter == "(AND: )" or has_acceptable_filter or not filter %}
                {% if not table.order_by %}
                    {% for i in record.tree_depth|as_range %}<i class="mdi mdi-circle-small"></i>{% endfor %}
                {% endif %}
            {% endif %}
            {% if value %}
                <span class="badge" style="color: {{ value.color|fgcolor }}; background-color: #{{ value.color }}">
                    <a href="{{ value.get_absolute_url }}">{{ value }}</a>
                </span>
            {% else %}
                &mdash;
            {% endif %}
        """

    def __init__(self, *args, **kwargs):
        super().__init__(
            template_code=self.template_code,
            attrs={'td': {'class': 'text-nowrap'}},
            *args,
            **kwargs
        )

    def value(self, value):
        return value


class CustomNamedClaimColumn(tables.TemplateColumn):
    template_code = """
            {% load helpers %}
            {% if value %}
            Link to Claim
            {% else %}
            &mdash;
            {% endif %}
        """

    def __init__(self, *args, **kwargs):
        super().__init__(
            template_code=self.template_code,
            attrs={'td': {'class': 'text-nowrap'}},
            *args,
            **kwargs
        )


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
    status = tables.Column(
        order_by=('is_draft', 'start_date', 'end_date'),
    )

    class Meta(NetBoxTable.Meta):
        model = Reservation
        fields = (
            'pk', 'id', 'name', 'claim_count', 'contact', 'tenant', 'is_draft', 'status', 'start_date', 'end_date',
            'description')
        default_columns = ('name', 'contact', 'tenant', 'claim_count', 'start_date', 'end_date', 'is_draft', 'status')


class ReducedClaimTable(NetBoxTable):
    tag = CustomColoredMPTTColumn()
    restriction = ChoiceFieldColumn()
    claim = CustomNamedClaimColumn(
        linkify=True,
        verbose_name='Link',
        accessor='id',
        visible=True,
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'tag', 'restriction', 'claim', 'description',
        )
        default_columns = (
            'id', 'tag', 'restriction',  'description',
        )


class ClaimTable(NetBoxTable):
    tag = CustomColoredMPTTColumn()
    reservation = tables.Column(
        linkify=True
    )
    restriction = ChoiceFieldColumn()
    start_date = tables.Column(accessor='reservation.start_date')
    end_date = tables.Column(accessor='reservation.end_date')
    claim = CustomNamedClaimColumn(
        linkify=True,
        verbose_name='Link',
        accessor='id',
        visible=True,
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'reservation', 'tag', 'restriction', 'description', 'start_date', 'end_date','claim',
        )
        default_columns = (
            'tag', 'reservation', 'restriction', 'claim', 'start_date', 'end_date',
        )


class ExtendedClaimTable(NetBoxTable):
    reservation = tables.Column(
        linkify=True
    )
    restriction = ChoiceFieldColumn()
    start_date = tables.Column(accessor='reservation.start_date')
    end_date = tables.Column(accessor='reservation.end_date')
    reservation__tenant = tables.Column(accessor='reservation.tenant', linkify=True)
    reservation__contact = tables.Column(accessor='reservation.contact', linkify=True)
    reservation__status = tables.Column(verbose_name='Status')

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'reservation', 'reservation__tenant', 'reservation__contact', 'reservation__status', 'tag',
            'restriction', 'description', 'start_date', 'end_date',
        )
        default_columns = (
            'id', 'reservation', 'reservation__tenant', 'reservation__contact',
            'restriction', 'reservation__status', 'start_date', 'end_date',
        )


class TagOverviewTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    color = columns.ColorColumn()
    reservation_count = tables.Column(
        verbose_name='Reservations active now'
    )

    class Meta(NetBoxTable.Meta):
        model = Tag
        fields = ('pk', 'id', 'color', 'name', 'slug', 'description', 'reservation_count')
        default_columns = ('name', 'reservation_count')


class DeviceCollisionTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = Device
        fields = ('pk', 'id', 'name', 'tags')
        default_columns = ('name', 'tags')
