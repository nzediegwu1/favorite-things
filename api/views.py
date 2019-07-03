from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import Favourite, Category
from .serializers import FavouriteSerializer, CategorySerializer


class FavouriteViewSet(ModelViewSet):
    """
    Handles CRUD operations for Favourite resourses
    """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def destroy(self, request, pk, format=None):
        favourite = get_object_or_404(Favourite, pk=pk)
        favourite.deleted = True
        favourite.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # favourite post-update signal will save metadata in metadata table


class CategoryViewSet(ModelViewSet):
    """
    Handles CRUD for category resources
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, pk, format=None):
        category = Category.objects.filter(id=pk)
        if not category:
            raise Http404
        category = category.prefetch_related(
            Prefetch(
                'favourites',
                queryset=Favourite.objects.filter(deleted=False))).first()
        category_data = CategorySerializer(category).data
        favourite_data = FavouriteSerializer(
            category.favourites,
            many=True,
        ).data
        return Response({**category_data, 'favourites': favourite_data})


# define custom 404 responses for page not found