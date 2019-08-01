from rest_framework.test import APITestCase
from api.models import Category
from api.tests.mocks import brite_core, brite_core_update


class TestGetFavouriteAuditLog(APITestCase):
    favourite_id = 0

    def setUp(self):
        category = Category.objects.create(name='Company')
        response = self.client.post('/favourites',
                                    brite_core(category.id),
                                    format='json')
        self.favourite_id = response.data['id']
        url = f'/favourites/{self.favourite_id}'
        self.client.put(url, brite_core_update(category.id), format='json')
        self.client.delete(url)

    def test_get_audit_log_succeeds_with_existing_favourite_id(self):
        response = self.client.get(f'/favourites/{self.favourite_id}/logs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'BriteCore-Audit Log')
        self.assertEqual(len(response.data['data']), 3)

        delete_audit_log = response.data['data'][0]
        self.assertEqual(delete_audit_log['action'], 'delete')
        self.assertEqual(delete_audit_log['resource_id'], self.favourite_id)
        self.assertEqual(delete_audit_log['model'], 'favourite')
        self.assertEqual(delete_audit_log['before']['title'], 'BriteCore')
        self.assertEqual(delete_audit_log['after'], {})

        update_audit_log = response.data['data'][1]
        self.assertEqual(update_audit_log['action'], 'update')
        self.assertEqual(update_audit_log['before']['title'], 'Brite Core')
        self.assertEqual(update_audit_log['after']['title'], 'BriteCore')
        self.assertEqual(update_audit_log['before']['ranking'], 3)
        self.assertEqual(update_audit_log['after']['ranking'], 10)

        creation_audit_log = response.data['data'][2]
        self.assertEqual(creation_audit_log['action'], 'create')
        self.assertEqual(creation_audit_log['before'], {})
        self.assertEqual(creation_audit_log['after']['title'], 'Brite Core')
        self.assertTrue('created_date' in creation_audit_log['after'])
        self.assertTrue('modified_date' in creation_audit_log['after'])

    def test_get_audit_log_fails_with_unexisting_favourite_id(self):
        response = self.client.get(f'/favourites/4343434/logs')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],
                         'favourite with pk 4343434, does not exist')
