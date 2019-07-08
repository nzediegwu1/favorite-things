from rest_framework.test import APITestCase
from api.models import Category, Favourite
import json

new_friend = {
    'title': 'anthony',
    'description': 'buddy of life',
    'ranking': 1,
}


class CategoryEndpoints(APITestCase):
    friends_id = 0

    def setUp(self):
        new_category = Category.objects.create(name='friends')
        new_friend['category'] = new_category
        self.friends_id = new_category.id

    def test_get_categories_succeeds(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['name'], 'friends')
        self.assertTrue('favourites' not in response.data[0])
        self.assertTrue('count' in response.data[0])
        self.assertEqual(response.data[0]['count'], 0)

    def test_get_single_category_succeeds_with_valid_id(self):
        Favourite.objects.create(**new_friend)
        response = self.client.get(f'/categories/{self.friends_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['name'], 'friends')
        self.assertTrue('favourites' in response.data)
        self.assertIsInstance(response.data['favourites'], list)
        self.assertEqual(response.data['favourites'][0]['title'], 'anthony')
        self.assertTrue('created_date' in response.data['favourites'][0])

    def test_get_single_category_fails_with_unexistin_id(self):
        response = self.client.get('/categories/2000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_update_category_succeeds_with_valid_input(self):
        update_data = {'name': 'Good friends'}
        url = f'/categories/{self.friends_id}'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_update_category_fails_with_invalid_input(self):
        update_data = {'name': '90987sjfksdfsdf'}
        url = f'/categories/{self.friends_id}'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0],
                         'Should contain only alphabets')

    def test_update_category_fails_with_unexisting_id(self):
        update_data = {'name': 'Books'}
        url = '/categories/2343200'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_update_category_fails_without_any_valid_field(self):
        update_data = {'stuff': 'Books'}
        url = f'/categories/{self.friends_id}'
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field is required.')

    def test_create_category_succeeds_with_valid_data(self):
        new_category = {'name': 'Family'}
        response = self.client.post('/categories', new_category, format='json')
        self.assertEqual(response.data['name'], new_category['name'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['count'], 0)

    def test_create_category_fails_with_invalid_input(self):
        invalid_category = {'name': '90987sjfksdfsdf'}
        url = '/categories'
        response = self.client.post(url, data=invalid_category, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0],
                         'Should contain only alphabets')

    def test_create_category_fails_without_required_field(self):
        invalid_category = {'stuff': 'Books'}
        url = '/categories'
        response = self.client.post(url, data=invalid_category, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field is required.')
