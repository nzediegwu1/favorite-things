from copy import deepcopy
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import Favourite, Category, MetaData
from .serializers import (FavouriteSerializer, CategorySerializer,
                          GetCategorySerializer, MetadataSerializer)


class FavouriteViewSet(ModelViewSet):
    """
    Handles CRUD operations for Favourite resourses
    """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def validation_error(self, favourite, metadata):
        return {
            'errors': {
                'favourite': favourite.errors,
                'metadata': metadata.errors
            }
        }

    def destroy(self, request, pk, format=None):
        favourite = get_object_or_404(Favourite, pk=pk)
        favourite.deleted = True
        favourite.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk, format=None):
        metadata = MetaData.objects.filter(favourite=pk)
        json_metadata = MetadataSerializer(metadata, many=True).data
        message = f'successfully fetched metadata for favourite {pk}'
        return Response({'message': message, 'data': json_metadata})

    def create(self, request, format=None):
        serializer = FavouriteSerializer(data=request.data)
        metadata_schema = MetadataSerializer(data=request.data.get('metadata'),
                                             many=True)
        if not serializer.is_valid() or not metadata_schema.is_valid():
            return Response(self.validation_error(serializer, metadata_schema),
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        metadata_schema.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(ModelViewSet):
    """
    Handles CRUD for category resources
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        favourites = category.favourites.filter(deleted=False)
        category_data = GetCategorySerializer(category).data
        favourite_data = FavouriteSerializer(
            favourites,
            many=True,
        ).data
        return Response({**category_data, 'favourites': favourite_data})


class MetadataViewSet(ModelViewSet):
    queryset = MetaData.objects.all()
    serializer_class = MetadataSerializer
