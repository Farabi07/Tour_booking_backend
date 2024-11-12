
from django.urls import path
from booking.views import traveler_views as views


urlpatterns = [
	path('api/v1/traveler/all/', views.getAllTraveler),

	path('api/v1/traveler/without_pagination/all/', views.getAllTravelerWithoutPagination),

	path('api/v1/traveler/<int:pk>', views.getATraveler),

	path('api/v1/traveler/search/', views.searchTraveler),

	path('api/v1/traveler/create/', views.createTraveler),

	path('api/v1/traveler/update/<int:pk>', views.updateTraveler),

	path('api/v1/traveler/delete/<int:pk>', views.deleteTraveler),

    path('api/v1/cart/<int:cart_item_id>/add_traveler/', views.addTravelerToCart),
    
    path('api/v1/cart/<int:cart_id>/travelers/', views.getTravelersForCart),
    
    path('api/v1/order/<int:order_id>/associate_travelers/', views.associateTravelersWithOrder),
    
    path('api/v1/order/<int:order_id>/travelers/', views.viewTravelersByOrder),
]