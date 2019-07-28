from rest_framework.test import APITestCase
from api.models import Favourite, MetaData, Category
from ..mocks import (jellof_rice, color_metadata, invalie_metadata_2)


class TestDeleteFavourite(APITestCase):
    favourite_id = 0

    def setUp(self):
        new_category = Category.objects.create(name='Food')
        new_favourite = Favourite.objects.create(**jellof_rice(new_category))
        self.favourite_id = new_favourite.id

    def test_create_metadata_succeeds_with_valid_data(self):
        metadata = color_metadata(self.favourite_id)
        response = self.client.post('/metadata', metadata)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], metadata['name'])
        self.assertEqual(response.data['value'], metadata['value'])

    def test_create_metadata_fails_with_invalid_data(self):
        response = self.client.post('/metadata', invalie_metadata_2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0],
                         "Ensure this field has no more than 30 characters.")
        self.assertEqual(response.data['data_type'][0],
                         "\"wonderful\" is not a valid choice.")
        self.assertEqual(response.data['value'][0], "Not a valid string.")

    def test_create_metadata_fails_without_required_fields(self):
        response = self.client.post('/metadata', {})
        message = "This field is required."
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], message)
        self.assertEqual(response.data['data_type'][0], message)
        self.assertEqual(response.data['value'][0], message)
