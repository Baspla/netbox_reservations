from netbox.filtersets import NetBoxModelFilterSet
from .models import Workspace


class WorkspaceFilterSet(NetBoxModelFilterSet):

    #start_before = DateFilter(name='start_date',lookup_type=('gt'),)
    #start_after = DateFilter(name='start_date',lookup_type=('lt'),)
    #end_before = DateFilter(name='end_date',lookup_type=('gt'))
    #end_after = DateFilter(name='end_date',lookup_type=('lt'))
    class Meta:
        model = Workspace
        fields = ('id','tenant','used_tags','start_date','end_date')

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
