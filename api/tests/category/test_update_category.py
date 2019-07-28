from rest_framework.test import APITestCase
from api.models import Category


class TestUpdateCategory(APITestCase):
    category_id = 0

    def setUp(self):
        new_category = Category.objects.create(name='food')
        self.category_id = new_category.id

    def test_update_category_succeeds_with_valid_input(self):
        update_data = {'name': 'Best food'}
        url = f'/categories/{self.category_id}'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_update_category_fails_with_invalid_input(self):
        update_data = {'name': []}
        url = f'/categories/{self.category_id}'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0],
                         'Not a valid string.')

    def test_update_category_fails_with_unexisting_id(self):
        update_data = {'name': 'Books'}
        url = '/categories/2343200'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_update_category_fails_without_any_valid_field(self):
        update_data = {'stuff': 'Books'}
        url = f'/categories/{self.category_id}'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field is required.')
