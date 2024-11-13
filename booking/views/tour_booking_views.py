from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

# from booking.decorators import has_permissions
from booking.models import Tour
from booking.serializers import TourSerializer, TourListSerializer
from booking.filters import TourFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination

# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=TourSerializer,
	responses=TourSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllTour(request):
	tours = Tour.objects.all()
	total_elements = tours.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	tours = pagination.paginate_data(tours)

	serializer = TourListSerializer(tours, many=True)

	response = {
		'tours': serializer.data,
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
	request=TourSerializer,
	responses=TourSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllTourWithoutPagination(request):
	tours = Tour.objects.all()

	serializer = TourListSerializer(tours, many=True)

	return Response({'tours': serializer.data}, status=status.HTTP_200_OK)


@extend_schema(request=TourSerializer, responses=TourSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getATour(request, pk):
	try:
		Tour = Tour.objects.get(pk=pk)
		serializer = TourSerializer(Tour)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Tour id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=TourSerializer, responses=TourSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchTour(request):
	tours = TourFilter(request.GET, queryset=Tour.objects.all())
	tours = tours.qs

	print('searched_products: ', tours)

	total_elements = tours.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	tours = pagination.paginate_data(tours)

	serializer = TourListSerializer(tours, many=True)

	response = {
		'tours': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(tours) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no tours matching your search"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=TourSerializer, responses=TourSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createTour(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = TourSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=TourSerializer, responses=TourSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateTour(request,pk):
	try:
		tours = Tour.objects.get(pk=pk)
		data = request.data
		serializer = TourSerializer(tours, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Tour id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=TourSerializer, responses=TourSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteTour(request, pk):
	try:
		Tour = Tour.objects.get(pk=pk)
		Tour.delete()
		return Response({'detail': f'Tour id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Tour id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
    ],
    request=TourListSerializer,
    responses=TourListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAvailableTours(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Filter tours based on start and end dates
    if start_date and end_date:
        tours = Tour.objects.filter(available_date__range=[start_date, end_date])
    elif start_date:
        tours = Tour.objects.filter(available_date__gte=start_date)
    elif end_date:
        tours = Tour.objects.filter(available_date__lte=end_date)
    else:
        return Response({"error": "Please provide a start or end date"}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total elements before pagination
    total_elements = tours.count()  # Count the items before pagination

    # Initialize pagination
    page = request.GET.get("page")
    size = request.GET.get("size")
    pagination = Pagination()
    pagination.page = page
    pagination.size = size

    # Apply pagination to the queryset
    paginated_tours = pagination.paginate_data(tours)

    # Serialize the paginated data
    serializer = TourListSerializer(paginated_tours, many=True)
    response = {
        'tours': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,  # Total elements before pagination
    }
    return Response(response, status=status.HTTP_200_OK)
