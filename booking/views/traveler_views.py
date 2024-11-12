from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

# from booking.decorators import has_permissions
from booking.models import Traveler
from booking.serializers import TravelerSerializer, TravelerListSerializer
from booking.filters import TravelerFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination
from order.models import CartItem,Cart,Order



# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=TravelerSerializer,
	responses=TravelerSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllTraveler(request):
	travelers = Traveler.objects.all()
	total_elements = travelers.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	travelers = pagination.paginate_data(travelers)

	serializer = TravelerListSerializer(travelers, many=True)

	response = {
		'travelers': serializer.data,
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
	request=TravelerSerializer,
	responses=TravelerSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllTravelerWithoutPagination(request):
	travelers = Traveler.objects.all()

	serializer = TravelerListSerializer(travelers, many=True)

	return Response({'travelers': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(request=TravelerListSerializer, responses=TravelerListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getATraveler(request, pk):
	try:
		travelers = Traveler.objects.get(pk=pk)
		serializer = TravelerListSerializer(travelers)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Traveler id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=TravelerListSerializer, responses=TravelerListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchTraveler(request):
	travelers = TravelerFilter(request.GET, queryset=Traveler.objects.all())
	travelers = travelers.qs

	print('searched_products: ', travelers)

	total_elements = travelers.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	travelers = pagination.paginate_data(travelers)

	serializer = TravelerListSerializer(travelers, many=True)

	response = {
		'travelers': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(travelers) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no travelers matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TravelerSerializer, responses=TravelerSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createTraveler(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = TravelerSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TravelerSerializer, responses=TravelerSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateTraveler(request,pk):
	try:
		travelers = Traveler.objects.get(pk=pk)
		data = request.data
		serializer = TravelerSerializer(travelers, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Traveler id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=TravelerSerializer, responses=TravelerSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteTraveler(request, pk):
	try:
		Traveler = Traveler.objects.get(pk=pk)
		Traveler.delete()
		return Response({'detail': f'Traveler id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Traveler id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=TravelerListSerializer, responses=TravelerListSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def addTravelerToCart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['booking'] = cart_item.tour.id  # Link traveler to the tour associated with the cart item

    serializer = TravelerListSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=TravelerListSerializer, responses=TravelerListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getTravelersForCart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    travelers = Traveler.objects.filter(booking__in=[item.tour.id for item in cart.items.all()])
    serializer = TravelerListSerializer(travelers, many=True)
    return Response({'travelers': serializer.data}, status=status.HTTP_200_OK)

@extend_schema(request=None, responses=TravelerListSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def associateTravelersWithOrder(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        travelers = Traveler.objects.filter(booking__in=[item.tour.id for item in order.cart.items.all()])
        
        # Update traveler records to associate them with this order, if necessary
        for traveler in travelers:
            traveler.booking = order.cart  # Assuming "booking" refers to the cart or order's tour
            traveler.save()

        serializer = TravelerListSerializer(travelers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
	
@extend_schema(request=TravelerListSerializer, responses=TravelerListSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def viewTravelersByOrder(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    travelers = Traveler.objects.filter(booking__in=[item.tour.id for item in order.cart.items.all()])
    serializer = TravelerListSerializer(travelers, many=True)
    return Response({'travelers': serializer.data}, status=status.HTTP_200_OK)