from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

# from order.decorators import has_permissions
from order.models import CartItem
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
	request=CartItemSerializer,
	responses=CartItemSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCartItem(request):
	cart_items = CartItem.objects.all()
	total_elements = cart_items.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	cart_items = pagination.paginate_data(cart_items)

	serializer = CartItemListSerializer(cart_items, many=True)

	response = {
		'cart_items': serializer.data,
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
	request=CartItemSerializer,
	responses=CartItemSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCartItemWithoutPagination(request):
	cart_items = CartItem.objects.all()

	serializer = CartItemListSerializer(cart_items, many=True)

	return Response({'cart_items': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=CartItemListSerializer, responses=CartItemListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getACartItem(request, pk):
	try:
		cart_items = CartItem.objects.get(pk=pk)
		serializer = CartItemListSerializer(cart_items)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"CartItem id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CartItemSerializer, responses=CartItemSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchCartItem(request):
	cart_items = CartItemFilter(request.GET, queryset=CartItem.objects.all())
	cart_items = cart_items.qs

	print('searched_products: ', cart_items)

	total_elements = cart_items.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	cart_items = pagination.paginate_data(cart_items)

	serializer = CartItemListSerializer(cart_items, many=True)

	response = {
		'cart_items': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(cart_items) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no cart_items matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CartItemSerializer, responses=CartItemSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createCartItem(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = CartItemSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CartItemSerializer, responses=CartItemSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateCartItem(request,pk):
	try:
		cart_items = CartItem.objects.get(pk=pk)
		data = request.data
		serializer = CartItemSerializer(cart_items, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"CartItem id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CartItemSerializer, responses=CartItemSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteCartItem(request, pk):
	try:
		cart_items = CartItem.objects.get(pk=pk)
		cart_items.delete()
		return Response({'detail': f'CartItem id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"CartItem id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=CartItemSerializer, responses=CartItemListSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addMultipleCartItems(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    items_data = request.data.get("items", [])
    created_items = []
    for item_data in items_data:
        item_data["cart"] = cart.id
        serializer = CartItemSerializer(data=item_data)
        if serializer.is_valid():
            serializer.save()
            created_items.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"added_items": created_items}, status=status.HTTP_201_CREATED)


@extend_schema(request=None, responses={"total_price": "Decimal"})
@api_view(['GET'])
def getCartTotalPrice(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    # Calculate total price by iterating over each CartItem and summing the prices
    total_price = sum(
        (item.tour.adult_price * item.quantity_adult) + (item.tour.child_price * item.quantity_child)
        for item in cart.items.all()  # Assuming `items` is the related_name for CartItem in Cart model
    )

    return Response({"cart_id": cart_id, "total_price": total_price}, status=status.HTTP_200_OK)

@extend_schema(request=None, responses={"detail": "All items cleared"})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clearCartItems(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    cart.items.all().delete()
    return Response({"detail": f"All items in cart {cart_id} have been cleared."}, status=status.HTTP_200_OK)
