from rest_framework import serializers
from .models import Favourite, Category, MetaData


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('id', 'title', 'description', 'ranking', 'created_date',
                  'modified_date', 'category')


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = ('id', 'name', 'data_type', 'value', 'favourite')


class FavouriteMetaSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(many=True, read_only=True)

    class Meta:
        model = Favourite
        fields = ('id', 'title', 'description', 'ranking', 'category',
                  'metadata')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'count')


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'count', 'favourites')
