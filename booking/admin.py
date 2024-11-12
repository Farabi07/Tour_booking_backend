from django.contrib import admin

from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Tour._meta.fields]

@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Traveler._meta.fields]

