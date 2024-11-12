

from django.urls import path
from booking.views import tour_booking_views as views


urlpatterns = [
	path('api/v1/tour/all/', views.getAllTour),

	path('api/v1/tour/without_pagination/all/', views.getAllTourWithoutPagination),

	path('api/v1/tour/<int:pk>', views.getATour),

	path('api/v1/tour/search/', views.searchTour),

	path('api/v1/tour/create/', views.createTour),

	path('api/v1/tour/update/<int:pk>', views.updateTour),

	path('api/v1/tour/delete/<int:pk>', views.deleteTour),
    
	path('api/v1/available_tour/with_pagination/all/', views.getAvailableTours),

#     path('api/v1/tour/book/<int:pk>/', views.bookTour, name='book_tour'),  # Example for booking a tour
#     path('api/v1/tour/cancel/<int:pk>/', views.cancelTourBooking, name='cancel_tour_booking'),  # Example for canceling a booking
#     path('api/v1/tour/review/<int:pk>/', views.addTourReview, name='add_tour_review'),  # Example for adding a review
 ]