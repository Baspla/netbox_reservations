from django import forms
from tenancy.models import Contact, Tenant
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import Reservation, Claim, RestrictionChoices

class DateInput(forms.DateInput):
    input_type = 'date'

class ReservationForm(NetBoxModelForm):
    comments = CommentField()
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=True,
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
    )
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Reservation
        fields = ('name', 'comments', 'contact', 'tenant','start_date','end_date', 'tags')


class ClaimForm(NetBoxModelForm):
    reservation = DynamicModelChoiceField(
        queryset=Reservation.objects.all()
    )
    tag = DynamicModelChoiceField(
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Claim
        fields = (
            'reservation', 'tag', 'description', 'restriction', 'tags',
        )


class ClaimFilterForm(NetBoxModelFilterSetForm):
    model = Claim
    reservation = forms.ModelMultipleChoiceField(
        queryset=Reservation.objects.all(),
        required=False
    )
    tag = DynamicModelChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    restriction = forms.MultipleChoiceField(
        choices=RestrictionChoices,
        required=False
    )
