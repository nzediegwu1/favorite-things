from django.db.models.signals import pre_save
from django.db import connection
from django.dispatch import receiver
from django.utils import timezone
from .models import Favourite, Category, AuditLog
from .queries import conditionally_increment_ranking
from .serializers import FavouriteSerializer, CategorySerializer
from .helpers import list_get


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
    if not instance.id:  # creation
        last_favourite = list_get(Favourite.objects.all().order_by("-id"), 0)
        favourite_id = last_favourite.id + 1 if last_favourite else 1
        new = FavouriteSerializer(instance).data
        new['category'] = instance.category.name
        log = {
            'model': 'favourite',
            'action': 'create',
            'date': timezone.now(),
            'old': {},
            'new': new,
            'resource_id': favourite_id
        }
        return AuditLog.objects.create(**log)

    if instance.deleted:
        update = FavouriteSerializer(instance).data
        update['category'] = instance.category.name
        log = {
            'model': 'favourite',
            'action': 'delete',
            'date': timezone.now(),
            'old': update,
            'new': {},
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
        'old': old,
        'new': update,
        'resource_id': instance.id
    }
    AuditLog.objects.create(**log)


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.id:  # creation
        last_category = list_get(Category.objects.all().order_by("-id"), 0)
        category_id = last_category.id + 1 if last_category else 1
        new = CategorySerializer(instance).data
        log = {
            'model': 'category',
            'action': 'create',
            'date': timezone.now(),
            'old': {},
            'new': new,
            'resource_id': category_id
        }
        return AuditLog.objects.create(**log)

    if instance.deleted:
        update = CategorySerializer(instance).data
        log = {
            'model': 'category',
            'action': 'delete',
            'date': timezone.now(),
            'old': update,
            'new': {},
            'resource_id': instance.id
        }
        return AuditLog.objects.create(**log)

    update = CategorySerializer(instance).data
    old = CategorySerializer(Category.objects.get(pk=instance.id)).data
    log = {
        'model': 'favourite',
        'action': 'update',
        'date': timezone.now(),
        'old': old,
        'new': update,
        'resource_id': instance.id
    }
    AuditLog.objects.create(**log)
