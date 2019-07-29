from django.db.models.signals import pre_save
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
    if not instance.id:  # creation
        new = FavouriteSerializer(instance).data
        new['category'] = instance.category.name
        log = {
            'action': 'create',
            'date': timezone.now(),
            'old': {},
            'new': new
        }
        AuditLog.objects.create(**log)


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    pass
