from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Favourite, Category
from .serializers import FavouriteSerializer, CategorySerializer
from .helpers import log_data, conditionally_reorder_ranking


@receiver(pre_save, sender=Favourite)
def favourite_pre_save(sender, instance, *args, **kwargs):
    conditionally_reorder_ranking(instance)

    # create audit logs for favourite delete and update signals
    if instance.id:
        if instance.deleted:
            old_data = FavouriteSerializer(instance).data
            old_data['category'] = instance.category.name
            return log_data('favourite', 'delete', old_data, {}, instance)

        new_data = FavouriteSerializer(instance).data
        new_data['category'] = instance.category.name
        old_favourite = Favourite.objects.get(pk=instance.id)
        old_data = FavouriteSerializer(old_favourite).data
        old_data['category'] = old_favourite.category.name
        return log_data('favourite', 'update', old_data, new_data, instance)


@receiver(post_save, sender=Favourite)
def favourite_post_save(sender, instance, created, **kwargs):
    # create audit logs for favourite-creation signals
    if created:
        new = FavouriteSerializer(instance).data
        new['category'] = instance.category.name
        return log_data('favourite', 'create', {}, new, instance)


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    # create audit logs for category delete and update signals
    if instance.id:
        if instance.deleted:
            update = CategorySerializer(instance).data
            return log_data('category', 'delete', update, {}, instance)

        update = CategorySerializer(instance).data
        old = CategorySerializer(Category.objects.get(pk=instance.id)).data
        return log_data('category', 'update', old, update, instance)


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    # create audit logs for categiory-creation signals
    if created:
        new = CategorySerializer(instance).data
        return log_data('category', 'create', {}, new, instance)
