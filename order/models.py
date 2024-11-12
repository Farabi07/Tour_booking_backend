from django.db import models
from django.conf import settings
from booking.models import Tour, Traveler

class Cart(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('checked_out', 'Checked Out'),
        ('abandoned', 'Abandoned'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional primary traveler for guest contact information
    primary_traveler = models.ForeignKey(
        Traveler,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts",
        help_text="The main traveler or contact person for this cart"
    )

    # Session ID for non-logged-in users
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Status to indicate cart state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    

    def __str__(self):
        return f"Cart {self.id} - Status: {self.status} - Primary Traveler: {self.primary_traveler}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    quantity_adult = models.PositiveIntegerField(default=1)
    quantity_child = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)

    def __str__(self):
        return f"CartItem {self.id} - Cart: {self.cart.id} - Tour: {self.tour.name}"

    def total_price(self):
        # Calculate total price based on quantities and tour prices
        adult_total = self.quantity_adult * (self.tour.adult_price or 0)
        child_total = self.quantity_child * (self.tour.child_price or 0)
        return adult_total + child_total


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(max_length=20, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - Status: {self.status}"

    def save(self, *args, **kwargs):
        # Calculate the total price from CartItems if not already set
        if not self.total_price:
            self.total_price = sum(item.total_price() for item in self.cart.items.all())
        super().save(*args, **kwargs)
