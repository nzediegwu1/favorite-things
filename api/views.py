from copy import deepcopy
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Prefetch
from .models import Favourite, Category, MetaData
from .helpers import delete_and_return, get_audit_log
from .serializers import (FavouriteSerializer, FavouriteMetaSerializer,
                          CategorySerializer, GetCategorySerializer,
                          MetadataSerializer)


class FavouriteViewSet(ModelViewSet):
    """
    Handles CRUD operations for Favourite resourses
    """
    queryset = Favourite.objects.filter(deleted=False)
    serializer_class = FavouriteSerializer

    def validation_error(self, favourite, metadata):
        return {
            'errors': {
                'favourite': favourite.errors,
                'metadata': metadata.errors if metadata else {}
            }
        }

    def destroy(self, request, pk, format=None):
        return delete_and_return(Favourite, pk)

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
    queryset = Category.objects.filter(deleted=False).order_by('-id')
    serializer_class = CategorySerializer

    def destroy(self, request, pk, format=None):
        return delete_and_return(Category, pk)

    def retrieve(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        favourites = category.favourites.filter(
            deleted=False).order_by('-modified_date')
        category_data = GetCategorySerializer(category).data
        favourite_data = FavouriteMetaSerializer(
            favourites,
            many=True,
        ).data
        return Response({**category_data, 'favourites': favourite_data})


class MetadataViewSet(ModelViewSet):
    queryset = MetaData.objects.all()
    serializer_class = MetadataSerializer

    def create(self, request, format=None):
        metadata_schema = MetadataSerializer(data=request.data)
        valid_metadata = metadata_schema.is_valid()
        if not valid_metadata:
            return Response(metadata_schema.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        favourite = get_object_or_404(Favourite, pk=request.data['favourite'])
        request.data['favourite'] = favourite
        metadata = MetaData.objects.create(**request.data)
        return Response(MetadataSerializer(metadata).data,
                        status=status.HTTP_201_CREATED)


class FavouriteAuditLog(APIView):
    def get(self, request, favourite_id, format=None):
        return get_audit_log(Favourite, favourite_id, 'favourite')


class CategoryAuditLog(APIView):
    def get(self, request, category_id, format=None):
        return get_audit_log(Category, category_id, 'category')


class LandingPage(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to favourite things'},
                        status=status.HTTP_200_OK)
