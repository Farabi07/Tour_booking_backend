from django_filters import rest_framework as filters

from payment.models import Payment



#Tour
class PaymentFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Payment
        fields = ['title', ]


