from django.db import models
from django.conf import settings

class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    adult_price = models.DecimalField(max_digits=8, decimal_places=2)
    child_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)


    def __str__(self):
        return f"{self.name} on {self.available_date}"

class Traveler(models.Model):
    booking = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="travelers",blank=True,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    is_child = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({'Child' if self.is_child else 'Adult'})"


