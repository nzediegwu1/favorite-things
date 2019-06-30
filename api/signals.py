from django.db.models.signals import pre_save
from django.db import connection
from django.dispatch import receiver
from .models import Favourite
from .queries import conditionally_increment_ranking


@receiver(pre_save, sender=Favourite)
def pre_save_handler(sender, instance, *args, **kwargs):
    same_ranking = Favourite.objects.filter(ranking=instance.ranking,
                                            category=instance.category,
                                            deleted=False)
    if same_ranking:
        from_ranking = instance.ranking - 1
        with connection.cursor() as cursor:
            cursor.execute(conditionally_increment_ranking,
                           [from_ranking, instance.category.id, False])
