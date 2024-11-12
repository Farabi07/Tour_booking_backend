from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

# from order.decorators import has_permissions
from order.models import Cart
from order.serializers import *
from order.filters import *
from booking.models import Tour,Traveler
from commons.enums import PermissionEnum
from commons.pagination import Pagination
from order.models import Order


# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=CartSerializer,
	responses=CartSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCart(request):
	carts = Cart.objects.all()
	total_elements = carts.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	carts = pagination.paginate_data(carts)

	serializer = CartListSerializer(carts, many=True)

	response = {
		'carts': serializer.data,
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
	request=CartSerializer,
	responses=CartSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCartWithoutPagination(request):
	carts = Cart.objects.all()

	serializer = CartListSerializer(carts, many=True)

	return Response({'carts': serializer.data}, status=status.HTTP_200_OK)

@extend_schema(request=CartListSerializer, responses=CartListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getACart(request, pk):
	try:
		carts = Cart.objects.get(pk=pk)
		serializer = CartListSerializer(carts)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Cart id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=CartSerializer, responses=CartSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchCart(request):
	carts = CartFilter(request.GET, queryset=Cart.objects.all())
	carts = carts.qs

	print('searched_products: ', carts)

	total_elements = carts.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	carts = pagination.paginate_data(carts)

	serializer = CartListSerializer(carts, many=True)

	response = {
		'carts': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(carts) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no carts matching your search"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=CartSerializer, responses=CartSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createCart(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = CartSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CartSerializer, responses=CartSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateCart(request,pk):
	try:
		Cart = Cart.objects.get(pk=pk)
		data = request.data
		serializer = CartSerializer(Cart, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Cart id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CartSerializer, responses=CartSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteCart(request, pk):
	try:
		Cart = Cart.objects.get(pk=pk)
		Cart.delete()
		return Response({'detail': f'Cart id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Cart id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=CartItemListSerializer, responses=CartItemListSerializer)
@api_view(['POST'])
def addCartItem(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['cart'] = cart.id

    try:
        tour = Tour.objects.get(id=data['tour_id'])
    except Tour.DoesNotExist:
        return Response({"error": "Tour not found"}, status=status.HTTP_404_NOT_FOUND)

    data['total_price'] = (tour.adult_price * data['quantity_adult']) + (tour.child_price * data['quantity_child'])
    
    serializer = CartItemListSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=CartListSerializer)
@api_view(['GET'])
def getCartItems(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    items = CartItem.objects.filter(cart=cart)
    serializer = CartItemListSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(request=CartListSerializer, responses=OrderListSerializer)
@api_view(['POST'])
def checkoutCart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    total_price = sum(item.total_price() for item in cart.items.all())
    order = Order.objects.create(cart=cart, status="pending", total_price=total_price)

    serializer = OrderListSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)