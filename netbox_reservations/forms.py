from django import forms

from tenancy.models import Contact, Tenant
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms import DynamicModelMultipleChoiceField
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import Reservation, Claim, RestrictionChoices


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ReservationForm(NetBoxModelForm):
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=True,
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
    )
    start_date = forms.DateTimeField(widget=DateTimeInput)
    end_date = forms.DateTimeField(widget=DateTimeInput)
    is_draft = forms.BooleanField(
        required=False,
        help_text='If checked, this reservation will be marked as a draft instead of planned/active/overdue.',
        initial=True
    )
    comments = CommentField()

    class Meta:
        model = Reservation
        fields = ('name', 'comments', 'contact', 'tenant', 'start_date', 'end_date', 'is_draft', 'tags')


class ClaimForm(NetBoxModelForm):
    reservation = DynamicModelChoiceField(
        queryset=Reservation.objects.all()
    )

    tag = DynamicModelChoiceField(
       queryset=Tag.objects.all()
    )

    parent = DynamicModelChoiceField(
        queryset=Claim.objects.all(),
        required=False
    )

    class Meta:
        model = Claim
        fields = (
            'reservation', 'tag', 'restriction', 'description',  'tags', 'parent'
        )


class ClaimFilterForm(NetBoxModelFilterSetForm):
    model = Claim
    reservation = DynamicModelMultipleChoiceField(
        queryset=Reservation.objects.all(),
        required=False
    )

    # Tag filter is not working yet (picks id but filters for slug)
    tag = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    restriction = forms.MultipleChoiceField(
        choices=RestrictionChoices,
        required=False
    )


class ReservationFilterForm(NetBoxModelFilterSetForm):
    model = Reservation
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    start_date = forms.DateTimeField(
        label='Start date after',
        widget=DateTimeInput,
        required=False
    )
    end_date = forms.DateTimeField(
        label='End date before',
        widget=DateTimeInput,
        required=False
    )
