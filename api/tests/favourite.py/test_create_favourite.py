# from rest_framework.test import APITestCase


# class TestCreateFavourite(APITestCase):
#     category_id = 0
#     url = '/favourites'

#     def setUp(self):
#         new_category = Category.objects.create(name='friends')
#         self.category_id = new_category.id

#     def test_create_favourite_succeeds_with_valid_data(self):
#         new_favourite = {'name': 'Family'}
#         response = self.client.post(self.url, new_favourite, format='json')
#         self.assertEqual(response.data['name'], new_favourite['name'])
#         self.assertEqual(response.status_code, 201)

#     def test_create_favourite_fails_with_invalid_input_data(self):
#         invalid = {'name': '90987sjfksdfsdf'}
#         response = self.client.post(self.url, data=invalid, format='json')
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data['name'][0],
#                          'Should contain only alphabets')

#     def test_create_category_fails_without_required_fields(self):
#         invalid = {'stuff': 'Books'}
#         response = self.client.post(self.url, data=invalid, format='json')
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.data['name'][0], 'This field is required.')
