from rest_framework import serializers
from .models import Cart, CartItem, Order
from django_currentuser.middleware import get_current_authenticated_user
from booking.serializers import TourSerializer, TourListSerializer

class CartMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = []  # Specify minimal fields or use fields = '__all__' if you want all fields

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        modelObject = super().create(validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.created_by = user
        modelObject.save()
        return modelObject

    def update(self, instance, validated_data):
        modelObject = super().update(instance=instance, validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.updated_by = user
        modelObject.save()
        return modelObject

class CartListSerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField()  # Use this if you want to list tours in the response
    total_item = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(read_only=True)
    updated_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else obj.created_by

    def get_updated_by(self, obj):
        return obj.updated_by.email if obj.updated_by else obj.updated_by

    def get_total_item(self, obj):
        # Count the number of items in the cart
        return obj.items.count()

    def get_total_cost(self, obj):
        # Calculate total cost by summing each item's total price in the cart
        total_cost = 0
        for item in obj.items.all():  # Assuming Cart has a related_name='items' to CartItem
            total_cost += (item.tour.adult_price * item.quantity_adult) + \
                          (item.tour.child_price * item.quantity_child)
        return total_cost

    def get_tours(self, obj):
        # Optionally, return a list of tour IDs or details for the tours in the cart
        return [item.tour.id for item in obj.items.all()] if obj.items.exists() else []

class CartItemMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = []  # Specify minimal fields or use fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        modelObject = super().create(validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.created_by = user
        modelObject.save()
        return modelObject

    def update(self, instance, validated_data):
        modelObject = super().update(instance=instance, validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.updated_by = user
        modelObject.save()
        return modelObject

class CartItemListSerializer(serializers.ModelSerializer):
    tour = TourListSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(read_only=True)
    updated_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['tour', 'quantity_adult', 'quantity_child', 'total_price', 'created_by', 'updated_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

    def get_total_price(self, obj):
        return (obj.tour.adult_price * obj.quantity_adult) + (obj.tour.child_price * obj.quantity_child) if obj.tour else 0

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else None
        
    def get_updated_by(self, obj):
        return obj.updated_by.email if obj.updated_by else None

class OrderMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = []  # Specify minimal fields or use fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        modelObject = super().create(validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.created_by = user
        modelObject.save()
        return modelObject

    def update(self, instance, validated_data):
        modelObject = super().update(instance=instance, validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.updated_by = user
        modelObject.save()
        return modelObject

class OrderListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()  # Changed to SerializerMethodField

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'created_at', 'created_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else None

    def get_total_price(self, obj):
        # Calculate total price by summing the total price of each CartItem in the cart
        return sum(
            (item.quantity_adult * (item.tour.adult_price or 0)) + 
            (item.quantity_child * (item.tour.child_price or 0))
            for item in obj.cart.items.all()
        )
