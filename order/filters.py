from django_filters import rest_framework as filters

from order.models import Cart,CartItem,Order


#Cart
class CartFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Cart
        fields = ['title', ]


# CartItem

class CartItemFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = CartItem
        fields = ['title', ]
# MetaData
class OrderFilter(filters.FilterSet):
    meta_title = filters.CharFilter(field_name="meta_title", lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['meta_title', ]
