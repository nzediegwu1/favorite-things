from django.db.models.signals import pre_save, post_save
from django.db import connection
from django.dispatch import receiver
from django.utils import timezone
from .models import Favourite, Category, AuditLog
from .queries import conditionally_increment_ranking
from .serializers import FavouriteSerializer, CategorySerializer


@receiver(pre_save, sender=Favourite)
def favourite_pre_save(sender, instance, *args, **kwargs):
    same_ranking = Favourite.objects.filter(
        ranking=instance.ranking,
        category=instance.category,
        deleted=False,
    ).exclude(id=instance.id)
    if same_ranking:
        from_ranking = instance.ranking - 1
        with connection.cursor() as cursor:
            cursor.execute(conditionally_increment_ranking,
                           [from_ranking, instance.category.id, False])
    if instance.id:  # update or soft-delete
        if instance.deleted:
            update = FavouriteSerializer(instance).data
            update['category'] = instance.category.name
            log = {
                'model': 'favourite',
                'action': 'delete',
                'date': timezone.now(),
                'before': update,
                'after': {},
                'resource_id': instance.id
            }
            return AuditLog.objects.create(**log)

        update = FavouriteSerializer(instance).data
        update['category'] = instance.category.name
        old = FavouriteSerializer(Favourite.objects.get(pk=instance.id)).data
        log = {
            'model': 'favourite',
            'action': 'update',
            'date': timezone.now(),
            'before': old,
            'after': update,
            'resource_id': instance.id
        }
        AuditLog.objects.create(**log)


@receiver(post_save, sender=Favourite)
def favourite_post_save(sender, instance, created, **kwargs):
    if created:
        new = FavouriteSerializer(instance).data
        new['category'] = instance.category.name
        log = {
            'model': 'favourite',
            'action': 'create',
            'date': instance.created_date,
            'before': {},
            'after': new,
            'resource_id': instance.id
        }
        return AuditLog.objects.create(**log)


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if instance.id:  # update or soft-delete
        if instance.deleted:
            update = CategorySerializer(instance).data
            log = {
                'model': 'category',
                'action': 'delete',
                'date': timezone.now(),
                'before': update,
                'after': {},
                'resource_id': instance.id
            }
            return AuditLog.objects.create(**log)

        update = CategorySerializer(instance).data
        old = CategorySerializer(Category.objects.get(pk=instance.id)).data
        log = {
            'model': 'category',
            'action': 'update',
            'date': timezone.now(),
            'before': old,
            'after': update,
            'resource_id': instance.id
        }
        AuditLog.objects.create(**log)


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    if created:
        new = CategorySerializer(instance).data
        log = {
            'model': 'category',
            'action': 'create',
            'date': timezone.now(),
            'before': {},
            'after': new,
            'resource_id': instance.id
        }
        return AuditLog.objects.create(**log)
