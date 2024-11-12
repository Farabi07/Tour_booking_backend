
from django.urls import path
from order.views import order_views as views


urlpatterns = [
	path('api/v1/order/all/', views.getAllOrder),

	path('api/v1/order/without_pagination/all/', views.getAllOrderWithoutPagination),

	path('api/v1/order/<int:pk>', views.getAOrder),

	path('api/v1/order/search/', views.searchOrder),

	path('api/v1/order/create/', views.createOrder),

	path('api/v1/order/update/<int:pk>', views.updateOrder),

	path('api/v1/order/delete/<int:pk>', views.deleteOrder),

    path('api/v1/order/<int:order_id>/calculate_total/', views.calculateOrderTotal),
    
    path('api/v1/order/<int:order_id>/initiate_payment/', views.initiateOrderPayment),
    
    path('api/v1/order/<int:order_id>/confirm_payment/', views.confirmOrderPayment),
]