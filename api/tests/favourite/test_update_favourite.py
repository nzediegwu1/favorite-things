from rest_framework.test import APITestCase
from api.models import Category, MetaData, Favourite
from ..mocks import (invalid_favourite, jellof_rice, spaghetti,
                     jellof_rice_update)


class TestUpdateFavourite(APITestCase):
    category_id = 0
    favourite_id = 0
    url = ''

    def setUp(self):
        new_category = Category.objects.create(name='food')
        new_favourite = Favourite.objects.create(**jellof_rice(new_category))
        self.favourite_id = new_favourite.id
        self.category_id = new_category.id
        self.url = f'/favourites/{new_favourite.id}'

    def test_update_favourite_succeeds_with_valid_data(self):
        """
        Test that endpoint to update a favourite succeeds when request body
        contain only valid data
        """
        update = jellof_rice_update(self.category_id)
        response = self.client.put(self.url, update, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], update['title'])
        self.assertEqual(self.category_id, response.data['category'])
        self.assertEqual(self.favourite_id, response.data['id'])
        self.assertTrue('created_date' in response.data)
        self.assertTrue('modified_date' in response.data)

    def test_update_favourite_fails_without_required_fields(self):
        empty_favourite = {}
        response = self.client.put(self.url,
                                   data=empty_favourite,
                                   format='json')
        self.assertEqual(response.status_code, 400)
        data = response.data
        for field in data:
            self.assertEqual(data[field][0], 'This field is required.')

    def test_update_favourite_fails_with_invalid_input_data(self):
        invalid_data = {**invalid_favourite}
        invalid_data['description'] = 'yay'
        response = self.client.put(self.url, data=invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['title'][0],
                         'Ensure this field has no more than 60 characters.')
        self.assertEqual(response.data['category'][0],
                         'Incorrect type. Expected pk value, received str.')
        self.assertEqual(response.data['description'][0],
                         'description should not be less than 10')
        self.assertEqual(response.data['ranking'][0],
                         'A valid integer is required.')
        self.assertEqual(response.data['category'][0],
                         'Incorrect type. Expected pk value, received str.')

    def test_update_favourite_fails_when_id_doesnt_exist(self):
        update = jellof_rice_update(self.category_id)
        response = self.client.put('/favourites/723', update, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_ranking_is_unique_reorders_if_duplicate(self):
        """
        Test that rankings for a given category is always unique and reorders
        when updated favourite has same ranking as an existing favourite
        """
        same_ranking_favourite = spaghetti(self.category_id)
        response = self.client.post('/favourites',
                                    same_ranking_favourite,
                                    format='json')
        # spaghetti ranking would be 1 while jellof-rice reorders to 2
        spags = Favourite.objects.get(pk=response.data['id'])
        jellof_rice = Favourite.objects.get(pk=self.favourite_id)
        self.assertEqual(spags.ranking, 1)
        self.assertEqual(jellof_rice.ranking, 2)

        # when Jellof-rice is updated to a ranking of 1, spaghetti ranking
        # reorders to 2
        update = jellof_rice_update(self.category_id)
        jellof_response = self.client.put(self.url, data=update, format='json')
        spags = Favourite.objects.get(pk=spags.id)
        self.assertEqual(spags.ranking, 2)
        self.assertEqual(jellof_response.data['ranking'], 1)

    def test_update_favourite_fails_with_unexisting_category(self):
        update = jellof_rice_update(9999999)
        response = self.client.put(self.url, update, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['category'][0],
                         "Invalid pk \"9999999\" - object does not exist.")
