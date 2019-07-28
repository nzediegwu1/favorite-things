from rest_framework.test import APITestCase
from api.models import Favourite, Category
from ..mocks import jellof_rice


class TestDeleteFavourite(APITestCase):
    favourite_id = 0
    url = ''

    def setUp(self):
        new_category = Category.objects.create(name='Food')
        new_favourite = Favourite.objects.create(**jellof_rice(new_category))
        self.favourite_id = new_favourite.id
        self.url = f'/favourites/{new_favourite.id}'

    def test_delete_favourite_succeeds_with_valid_id(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        deleted_favourite = Favourite.objects.get(pk=self.favourite_id)
        self.assertTrue(deleted_favourite.deleted)

    def test_delete_favourite_fails_with_invalid_id(self):
        response = self.client.delete('/favourites/sjdks92323')
        self.assertEqual(response.status_code, 404)

    def test_delete_favourite_fails_with_unexisting_id(self):
        response = self.client.delete('/favourites/9999999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')
