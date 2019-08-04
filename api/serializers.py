from rest_framework import serializers
from .models import Favourite, Category, MetaData, AuditLog


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
    metadata = MetadataSerializer(many=True, read_only=False)

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


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'model', 'action', 'date', 'before', 'after',
                  'resource_id')
