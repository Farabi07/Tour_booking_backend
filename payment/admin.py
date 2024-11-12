from django.contrib import admin

from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Payment._meta.fields]