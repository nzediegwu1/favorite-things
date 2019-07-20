from rest_framework.test import APITestCase


class TestCreateCategory(APITestCase):
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
