from rest_framework.response import Response
from rest_framework import status


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
