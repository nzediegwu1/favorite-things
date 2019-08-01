from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import connection
from .models import AuditLog, Favourite
from .queries import conditionally_increment_ranking


def delete_and_return(model, pk):
    """Soft-deletes a record and returns a HTTP response

    Args:
        model(cls): model of the entity to remove
        pk(number): id of the record to delete
    Returns:
        object: HTTP response with 404 or 204 status code
    """
    model.soft_delete(pk)
    return Response(status=status.HTTP_204_NO_CONTENT)


def log_data(model, action, before, after, instance):
    """Logs mutation signals for Favourite and Category models

    Args:
        model(str): the target class of the audit-log: favourite or category
        action(str): the type of mutation to be logged: create, update, delete
        before(dict): the previous value of the data mutated
        after(dict): the new value of the data mutated
        instance(object): the favourite or category instance being mutated

    Returns:
        object: instance of AuditLog created for the mutation
    """
    log = {
        'model': model,
        'action': action,
        'date': timezone.now(),
        'before': before,
        'after': after,
        'resource_id': instance.id
    }
    return AuditLog.objects.create(**log)


def conditionally_reorder_ranking(instance):
    """Reorder rankings of favourites in same category if an existing favourite
    has same ranking with current favourite

    Args:
        instance(object): the favourite instance to be saved
    """
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
