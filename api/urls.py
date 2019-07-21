from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FavouriteViewSet, CategoryViewSet, MetadataViewSet

router = DefaultRouter()

list_bindings = {'get': 'list', 'post': 'create'}
single_bindings = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
update_delete_bindings = {'put': 'update', 'delete': 'destroy'}

create_favourite = FavouriteViewSet.as_view({'post': 'create'})
single_favourite = FavouriteViewSet.as_view(update_delete_bindings)
category_list = CategoryViewSet.as_view(list_bindings)
single_category = CategoryViewSet.as_view(single_bindings)
delete_metadata = MetadataViewSet.as_view({'delete': 'destroy'})
create_metadata = MetadataViewSet.as_view({'post': 'create'})
single_favourite_metadata = FavouriteViewSet.as_view({'get': 'retrieve'})

urlpatterns = format_suffix_patterns([
    path('favourites', create_favourite, name='create-favourite'),
    path('favourites/<int:pk>', single_favourite, name='single-favourite'),
    path('favourites/<int:pk>/metadata',
         single_favourite_metadata,
         name='single-favourite-metadata'),
    path('categories', category_list, name='category-list'),
    path('categories/<int:pk>', single_category, name='single-category'),
    path('metadata/<int:pk>', delete_metadata, name='delete-metadata'),
    path('metadata', create_metadata, name='create-metadata'),
])
