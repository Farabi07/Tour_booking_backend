from rest_framework import serializers
from .models import Payment
from django.conf import settings
from rest_framework_recursive.fields import RecursiveField
from django_currentuser.middleware import get_current_authenticated_user
from authentication.serializers import AdminUserMinimalListSerializer
from booking.serializers import TourSerializer
from .serializers import *


class PaymentListSerializer(serializers.ModelSerializer):
    payment_status = serializers.CharField(source='status', read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)
    updated_by = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'created_at':{
                'read_only': True,
            },
            'updated_at':{
                'read_only': True,
            },
            'created_by':{
                'read_only': True,
            },
            'updated_by':{
                'read_only': True,
            },
        }

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else obj.created_by
        
    def get_updated_by(self, obj):
        return obj.updated_by.email if obj.updated_by else obj.updated_by
	


class PaymentMinimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = ('',)

class PaymentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Payment
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