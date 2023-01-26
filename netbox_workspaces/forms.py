from extras.models import Tag
from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelMultipleChoiceField, DynamicModelChoiceField
from .models import Workspace


class DateInput(forms.DateInput):
    input_type = 'date'


class WorkspaceForm(NetBoxModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    used_tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=True,
    )

    comments = CommentField()

    class Meta:
        model = Workspace
        fields = ('name', 'description', 'tenant','start_date', 'end_date', 'used_tags', 'comments','tags')

class WorkspaceFilterForm(NetBoxModelFilterSetForm):
    model = Workspace
   # start_before = forms.DateField(widget=DateInput,
   #     required=False,)
   # start_after = forms.DateField(widget=DateInput,
   #     required=False,)
   # end_before = forms.DateField(widget=DateInput,
   #     required=False,)
   # end_after = forms.DateField(widget=DateInput,
   #     required=False,)

    start_date = forms.DateField(widget=DateInput,
     required=False,)
    end_date = forms.DateField(widget=DateInput,
     required=False,)

    used_tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )
