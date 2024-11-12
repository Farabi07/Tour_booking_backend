from django.urls import path
from payment.views import payment_views as views

urlpatterns = [
    path('api/v1/payment/all/', views.getAllPayment),
    
    path('api/v1/payment/without_pagination/all/', views.getAllPaymentWithoutPagination),
    
    path('api/v1/payment/<int:pk>', views.getAPayment),
    
    path('api/v1/payment/search/', views.searchPayment),
    
    path('api/v1/payment/update/<int:pk>', views.updatePayment),
    
    path('api/v1/payment/delete/<int:pk>', views.deletePayment),
    
    path('api/v1/order/<int:order_id>/payment/', views.createPayment),

    path('api/v1/order/<int:order_id>/confirm-payment/', views.confirmOrderPayment), 
]
