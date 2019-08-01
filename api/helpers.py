from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import connection
from rest_framework.exceptions import NotFound
from .models import AuditLog, Favourite
from .serializers import AuditLogSerializer
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


def custom_get_or_404(model, pk, message):
    """Get a record or return 404 http response with custom message

    Args:
        model(cls): django class representing the database table to query
        pk(int): the primary key of the resource to find
        message(str): the error message to use in the 404 response
    Returns:
        object: instance of the record retrieved
    """
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise NotFound(message, 404)


def get_audit_log(model, pk, model_key):
    """Retrieves audit-log for a given resource or raise 404 error

    Args:
        model(cls): django class representing the database table to query
        pk(int): the primary key of the resource to retrieve audit-log for
        model_key(str): string key representing the resource type. eg: category or favourite

    Returns
        object: http response with audit-log data and 200 status code
    
    Raises:
        exception: which resolves to 404 http response if the target resource does not exist
    """
    custom_get_or_404(model, pk, f"{model_key} with pk {pk}, does not exist")
    logs = AuditLog.objects.filter(model=model_key,
                                   resource_id=pk).order_by('-id')
    log_data = AuditLogSerializer(logs, many=True).data
    instance = model.objects.get(pk=pk)
    response = {'message': f'{instance.__str__()}-Audit Log', 'data': log_data}
    return Response(response, status=status.HTTP_200_OK)
