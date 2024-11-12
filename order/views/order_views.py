from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

# from order.decorators import has_permissions
from order.models import Order
from order.serializers import *
from order.filters import *

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=OrderSerializer,
	responses=OrderSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllOrder(request):
	orders = Order.objects.all()
	total_elements = orders.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	orders = pagination.paginate_data(orders)

	serializer = OrderListSerializer(orders, many=True)

	response = {
		'orders': serializer.data,
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
	request=OrderSerializer,
	responses=OrderSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllOrderWithoutPagination(request):
	orders = Order.objects.all()

	serializer = OrderListSerializer(orders, many=True)

	return Response({'orders': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=OrderListSerializer, responses=OrderListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAOrder(request, pk):
	try:
		order = Order.objects.get(pk=pk)
		serializer = OrderListSerializer(order)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Order id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchOrder(request):
	orders = OrderFilter(request.GET, queryset=Order.objects.all())
	orders = orders.qs

	print('searched_products: ', orders)

	total_elements = orders.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	orders = pagination.paginate_data(orders)

	serializer = OrderListSerializer(orders, many=True)

	response = {
		'orders': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(orders) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no orders matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createOrder(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = OrderSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateOrder(request,pk):
	try:
		orders = Order.objects.get(pk=pk)
		data = request.data
		serializer = OrderSerializer(orders, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Order id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteOrder(request, pk):
	try:
		orders = Order.objects.get(pk=pk)
		orders.delete()
		return Response({'detail': f'Order id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Order id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
	
@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['GET'])
def calculateOrderTotal(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    total_price = sum(item.total_price() for item in order.cart.items.all())
    order.total_price = total_price
    order.save()

    return Response({"order_id": order.id, "total_price": total_price}, status=status.HTTP_200_OK)

@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['POST'])
def initiateOrderPayment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Assuming integration with Klarna or other payment gateway
    # Example: Create a payment session with a third-party payment provider
    payment_url = "https://payment-processor.com/pay/" + str(order_id)  # Example URL

    # Update order status to reflect payment initiation
    order.status = "payment_pending"
    order.save()

    return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)

@extend_schema(request=OrderSerializer, responses=OrderSerializer)
@api_view(['POST'])
def confirmOrderPayment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Example: Update order payment status after confirmation
    order.status = "paid"
    order.save()

    return Response({"detail": f"Order {order_id} payment confirmed and status updated to 'paid'."}, status=status.HTTP_200_OK)