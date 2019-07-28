from rest_framework.test import APITestCase
from api.models import Favourite, MetaData, Category
from ..mocks import jellof_rice, color_metadata


class TestDeleteFavourite(APITestCase):
    metadata_id = 0
    url = ''

    def setUp(self):
        new_category = Category.objects.create(name='Food')
        new_favourite = Favourite.objects.create(**jellof_rice(new_category))
        new_metadata = MetaData.objects.create(**color_metadata(new_favourite))
        self.metadata_id = new_metadata.id
        self.url = f'/metadata/{new_metadata.id}'

    def test_delete_metadata_succeeds_with_valid_id(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_delete_metadata_fails_with_invalid_id(self):
        response = self.client.delete('/metadata/sjdks92323')
        self.assertEqual(response.status_code, 404)

    def test_delete_metadata_fails_with_unexisting_id(self):
        response = self.client.delete('/metadata/9999999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')
