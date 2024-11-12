
from django.urls import path
from order.views import cart_views as views


urlpatterns = [
	path('api/v1/cart/all/', views.getAllCart),

	path('api/v1/cart/without_pagination/all/', views.getAllCartWithoutPagination),

	path('api/v1/cart/<int:pk>', views.getACart),

	path('api/v1/cart/search/', views.searchCart),

	path('api/v1/cart/create/', views.createCart),

	path('api/v1/cart/update/<int:pk>', views.updateCart),

	path('api/v1/cart/delete/<int:pk>', views.deleteCart),

    # New URL patterns for cart items
    path('api/v1/cart/<int:cart_id>/add-item/', views.addCartItem),
    
    path('api/v1/cart/<int:cart_id>/items/', views.getCartItems),

    # New URL pattern for checkout
    path('api/v1/cart/<int:cart_id>/checkout/', views.checkoutCart),
]