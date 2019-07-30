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


def list_get(array, index):
    """Retrieve an item in list or returns None if index is out of range

    Args:
        array(list): the list whose item is to be retrieved
        index(number): the index of the item to retrieve
    Returns:
        any: item retrieved from the array
    """
    return array[index] if len(array) > index else None
