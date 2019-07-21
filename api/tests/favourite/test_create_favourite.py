from rest_framework.test import APITestCase
from api.models import Category, MetaData, Favourite
from ..mocks import (egusi_soup, invalid_favourite, jellof_rice, spaghetti,
                     invalid_metadata)


class TestCreateFavourite(APITestCase):
    category_id = 0
    url = '/favourites'

    def setUp(self):
        new_category = Category.objects.create(name='food')
        self.category_id = new_category.id

    def test_create_favourite_succeeds_with_valid_data(self):
        """
        Test that endpoint to create new favourite succeeds and metadata are
        also saved for the favourite created
        """
        new_favourite = egusi_soup(self.category_id)
        response = self.client.post(self.url, new_favourite, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], new_favourite['title'])
        self.assertEqual(self.category_id, response.data['category'])
        fav_ingredient = new_favourite['metadata'][0]
        fav_duration = new_favourite['metadata'][1]
        ingredient = MetaData.objects.filter(
            name=fav_ingredient['name'],
            value=fav_ingredient['value']).first()
        duration = MetaData.objects.filter(
            name=fav_duration['name'], value=fav_duration['value']).first()
        self.assertEqual(duration.favourite_id, response.data['id'])
        self.assertEqual(ingredient.favourite_id, response.data['id'])

    def test_create_favourite_fails_with_invalid_input_data(self):
        response = self.client.post(self.url,
                                    data=invalid_favourite,
                                    format='json')
        self.assertEqual(response.status_code, 400)
        favourite_errors = response.data['errors']['favourite']
        self.assertEqual(favourite_errors['title'][0],
                         'Should contain only alphabets')
        self.assertEqual(favourite_errors['description'][0],
                         'Not a valid string.')
        self.assertEqual(favourite_errors['ranking'][0],
                         'A valid integer is required.')
        self.assertEqual(favourite_errors['category'][0],
                         'Incorrect type. Expected pk value, received str.')
        self.assertEqual(
            response.data['errors']['metadata']['non_field_errors'][0],
            "Expected a list of items but got type \"str\".")

    def test_create_favourite_fails_without_required_fields(self):
        empty_favourite = {'stuff': 'Books'}
        response = self.client.post(self.url,
                                    data=empty_favourite,
                                    format='json')
        self.assertEqual(response.status_code, 400)
        favourite_errors = response.data['errors']['favourite']
        self.assertEqual(favourite_errors['title'][0],
                         'This field is required.')
        self.assertEqual(favourite_errors['description'][0],
                         'This field is required.')
        self.assertEqual(favourite_errors['ranking'][0],
                         'This field is required.')
        self.assertEqual(favourite_errors['category'][0],
                         'This field is required.')
        self.assertEqual(response.data['errors']['metadata'], {})

    def test_create_favourite_succeeds_without_metadata(self):
        new_favourite = jellof_rice(self.category_id)
        response = self.client.post(self.url, new_favourite, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], new_favourite['title'])

    def test_ranking_is_unique_and_reorders_when_duplicate(self):
        """
        Test that rankings for a given category is always unique and reorders
        when new favourite has same ranking as with existing favourite
        """
        for favourite in [egusi_soup, jellof_rice, spaghetti]:
            new_favourite = favourite(self.category_id)
            self.client.post(self.url, new_favourite, format='json')

        food_favourites = Favourite.objects.filter(category=self.category_id)
        self.assertEqual(len(food_favourites), 3)
        rankings = [favourite.ranking for favourite in food_favourites]
        self.assertEqual(rankings, [3, 2, 1])

    def test_create_favourite_fails_with_invalid_metadata_fields(self):
        new_favourite = jellof_rice(self.category_id)
        new_favourite['metadata'] = invalid_metadata
        response = self.client.post(self.url,
                                    data=new_favourite,
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['favourite'], {})
        metadata_errors = response.data['errors']['metadata'][0]
        self.assertEqual(metadata_errors['name'][0],
                         'Should contain only alphabets')
        self.assertEqual(metadata_errors['data_type'][0],
                         '\"stuff\" is not a valid choice.')
        self.assertEqual(metadata_errors['value'][0], 'Not a valid string.')

    def test_create_metadata_fails_without_required_fields(self):
        new_favourite = jellof_rice(self.category_id)
        new_favourite['metadata'] = [{}]
        response = self.client.post(self.url,
                                    data=new_favourite,
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['favourite'], {})
        metadata_errors = response.data['errors']['metadata'][0]
        self.assertEqual(metadata_errors['name'][0], 'This field is required.')
        self.assertEqual(metadata_errors['data_type'][0],
                         'This field is required.')
        self.assertEqual(metadata_errors['value'][0],
                         'This field is required.')

    def test_create_favourite_fails_with_unexisting_category(self):
        new_favourite = egusi_soup(90293)
        response = self.client.post(self.url,
                                    data=new_favourite,
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['favourite']['category'][0],
                         "Invalid pk \"90293\" - object does not exist.")
