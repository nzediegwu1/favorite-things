from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Favourite, Category
from .serializers import FavouriteSerializer, CategorySerializer


class FavouriteViewSet(ModelViewSet):
    """
    Handles CRUD operations for Favourite resourses
    """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


class CategoryViewSet(ModelViewSet):
    """
    Handles CRUD for category resources
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
