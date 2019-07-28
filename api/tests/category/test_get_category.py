from rest_framework.test import APITestCase
from api.models import Category, Favourite

new_friend = {
    'title': 'anthony',
    'description': 'buddy of life',
    'ranking': 1,
}


class TestGetCategory(APITestCase):
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

    def test_get_single_category_fails_with_unexistin_id(self):
        response = self.client.get('/categories/2000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')
