
from django.urls import path
from order.views import cartItem_views as views


urlpatterns = [
	path('api/v1/cart_item/all/', views.getAllCartItem),

	path('api/v1/cart_item/without_pagination/all/', views.getAllCartItemWithoutPagination),

	path('api/v1/cart_item/<int:pk>', views.getACartItem),

	path('api/v1/cart_item/search/', views.searchCartItem),

	path('api/v1/cart_item/create/', views.createCartItem),

	path('api/v1/cart_item/update/<int:pk>', views.updateCartItem),

	path('api/v1/cart_item/delete/<int:pk>', views.deleteCartItem),

    path('api/v1/cart_item/add_multiple/<int:cart_id>/', views.addMultipleCartItems),
    
    path('api/v1/cart_item/total_price/<int:cart_id>/', views.getCartTotalPrice),
    
    path('api/v1/cart_item/clear/<int:cart_id>/', views.clearCartItems),
]