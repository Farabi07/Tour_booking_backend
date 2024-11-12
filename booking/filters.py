from django_filters import rest_framework as filters

from booking.models import Tour,Traveler



#Tour
class TourFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Tour
        fields = ['title', ]


# Traveler

class TravelerFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Traveler
        fields = ['title', ]
# # MetaData
# class MetaDataFilter(filters.FilterSet):
#     meta_title = filters.CharFilter(field_name="meta_title", lookup_expr='icontains')

#     class Meta:
#         model = MetaData
#         fields = ['meta_title', ]
