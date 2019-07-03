from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FavouriteViewSet, CategoryViewSet

router = DefaultRouter()

list_bindings = {'get': 'list', 'post': 'create'}
single_bindings = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}

favourite_list = FavouriteViewSet.as_view({'post': 'create'})
single_favourite = FavouriteViewSet.as_view({
    'put': 'update',
    'delete': 'destroy'
})

category_list = CategoryViewSet.as_view(list_bindings)
single_category = CategoryViewSet.as_view(single_bindings)

urlpatterns = format_suffix_patterns([
    path('favourites', favourite_list, name='favourite-list'),
    path('favourites/<int:pk>', single_favourite, name='single-favourite'),
    path('categories', category_list, name='category-list'),
    path('categories/<int:pk>', single_category, name='single-category'),
])