from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

# from Payment.decorators import has_permissions
from payment.models import Payment
from payment.serializers import *
from payment.filters import *

from commons.enums import PermissionEnum
from commons.pagination import Pagination
from order.models import Order
import requests
from order.serializers import OrderListSerializer


# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=PaymentSerializer,
	responses=PaymentSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllPayment(request):
	payments = Payment.objects.all()
	total_elements = payments.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	payments = pagination.paginate_data(payments)

	serializer = PaymentListSerializer(payments, many=True)

	response = {
		'payments': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=PaymentSerializer,
	responses=PaymentSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllPaymentWithoutPagination(request):
	payments = Payment.objects.all()

	serializer = PaymentListSerializer(payments, many=True)

	return Response({'payments': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAPayment(request, pk):
	try:
		Payment = Payment.objects.get(pk=pk)
		serializer = PaymentSerializer(Payment)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Payment id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchPayment(request):
	payments = PaymentFilter(request.GET, queryset=Payment.objects.all())
	payments = payments.qs

	print('searched_products: ', payments)

	total_elements = payments.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	payments = pagination.paginate_data(payments)

	serializer = PaymentListSerializer(payments, many=True)

	response = {
		'payments': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(payments) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no payments matching your search"}, status=status.HTTP_400_BAD_REQUEST)




# @extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# # @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
# def createPayment(request):
# 	data = request.data
# 	filtered_data = {}

# 	for key, value in data.items():
# 		if value != '' and value != '0':
# 			filtered_data[key] = value

# 	serializer = PaymentSerializer(data=filtered_data)

# 	if serializer.is_valid():
# 		serializer.save()
# 		return Response(serializer.data, status=status.HTTP_201_CREATED)
# 	else:
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updatePayment(request,pk):
	try:
		payments = Payment.objects.get(pk=pk)
		data = request.data
		serializer = PaymentSerializer(payments, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Payment id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deletePayment(request, pk):
	try:
		payments = Payment.objects.get(pk=pk)
		payments.delete()
		return Response({'detail': f'Payment id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Payment id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=OrderListSerializer, responses=PaymentSerializer)
@api_view(['POST'])
def createPayment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    payment_data = {
        "order_amount": int(order.total_price * 100),  # Klarna expects amount in cents
        "order_lines": [
            {
                "name": f"Order #{order.id}",
                "quantity": 1,
                "unit_price": int(order.total_price * 100),
                "total_amount": int(order.total_price * 100),
            }
        ],
        "merchant_urls": {
            "success": "https://yourwebsite.com/payment-success",
            "cancel": "https://yourwebsite.com/payment-cancel",
            "failure": "https://yourwebsite.com/payment-failure"
        }
    }
    # Klarna sandbox API endpoint
    klarna_sandbox_url = "https://api.playground.klarna.com/payments/v1/sessions"

    # Use Klarna sandbox credentials
    klarna_api_user = "YOUR_TEST_KLARNA_API_USER"       # Replace with your Klarna sandbox username
    klarna_api_password = "YOUR_TEST_KLARNA_API_PASSWORD"  # Replace with your Klarna sandbox password

    response = requests.post(
        "https://api.klarna.com/payments/v1/sessions", 
        json=payment_data,
        auth=("Klarna_API_User", "Klarna_API_Password")  # Replace with actual Klarna API credentials
    )

    if response.status_code == 200:
        payment_info = response.json()
        Payment.objects.create(
            order=order,
            payment_id=payment_info['payment_id'],
            status="initiated",
            amount=order.total_price
        )
        return Response({"redirect_url": payment_info['redirect_url']}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to create payment session"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=OrderListSerializer, responses=PaymentSerializer)
@api_view(['POST'])
def confirmOrderPayment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(order=order)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return Response({"error": "Order or Payment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Simulate or call Klarna's API to get the latest payment status
    klarna_response = requests.get(
        f"https://api.klarna.com/payments/v1/orders/{payment.payment_id}",  # Assuming this is Klarna’s endpoint
        auth=("Klarna_API_User", "Klarna_API_Password")  # Replace with actual Klarna credentials
    )

    if klarna_response.status_code == 200:
        klarna_data = klarna_response.json()
        payment_status = klarna_data.get('status')

        if payment_status == 'completed':  # Adjust status check based on Klarna's response structure
            # Update payment and order status to paid
            payment.status = 'completed'
            payment.save()

            order.status = 'paid'
            order.save()

            return Response({
                "detail": "Payment confirmed and order marked as paid",
                "order_id": order.id,
                "payment_id": payment.payment_id,
                "status": "paid"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Payment not completed yet",
                "status": payment_status
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Failed to retrieve payment status"}, status=status.HTTP_400_BAD_REQUEST)