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
                'metadata': metadata.errors if metadata else {}
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

    def meta_object(self, metadata, favourite):
        metadata['favourite'] = favourite
        return MetaData(**metadata)

    def create(self, request, format=None):
        favourite_schema = FavouriteSerializer(data=request.data)
        metadata = request.data.get('metadata')
        MetadataSerializer.Meta.fields = ('name', 'data_type', 'value')
        metadata_schema = MetadataSerializer(data=metadata,
                                             many=True) if metadata else None
        valid_favourite, valid_metadata = favourite_schema.is_valid(
        ), metadata_schema.is_valid() if metadata else True
        if not valid_favourite or not valid_metadata:
            errors = self.validation_error(favourite_schema, metadata_schema)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        favourite = favourite_schema.save()
        if metadata:
            bulk_metadata = [
                self.meta_object(item, favourite) for item in metadata
            ]
            MetaData.objects.bulk_create(bulk_metadata)
        return Response(favourite_schema.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(ModelViewSet):
    """
    Handles CRUD for category resources
    """
    queryset = Category.objects.all().order_by('-id')
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
