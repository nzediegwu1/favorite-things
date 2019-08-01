from rest_framework.test import APITestCase


class TestGetCategoryAuditLog(APITestCase):
    category_id = 0

    def setUp(self):
        category = {'name': 'Movies'}
        response = self.client.post('/categories', category, format='json')
        self.category_id = response.data['id']
        url = f'/categories/{self.category_id}'
        self.client.put(url, {'name': 'Action Movies'})
        self.client.delete(url)

    def test_get_audit_log_succeeds_with_existing_category_id(self):
        response = self.client.get(f'/categories/{self.category_id}/logs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Action Movies-Audit Log')
        self.assertEqual(len(response.data['data']), 3)

        delete_audit_log = response.data['data'][0]
        self.assertEqual(delete_audit_log['action'], 'delete')
        self.assertEqual(delete_audit_log['resource_id'], self.category_id)
        self.assertEqual(delete_audit_log['model'], 'category')
        self.assertEqual(delete_audit_log['before']['name'], 'Action Movies')
        self.assertEqual(delete_audit_log['after'], {})

        update_audit_log = response.data['data'][1]
        self.assertEqual(update_audit_log['action'], 'update')
        self.assertEqual(update_audit_log['before']['name'], 'Movies')
        self.assertEqual(update_audit_log['after']['name'], 'Action Movies')

        creation_audit_log = response.data['data'][2]
        self.assertEqual(creation_audit_log['action'], 'create')
        self.assertEqual(creation_audit_log['before'], {})
        self.assertEqual(creation_audit_log['after']['name'], 'Movies')

    def test_get_audit_log_fails_with_unexisting_category_id(self):
        response = self.client.get(f'/categories/4343434/logs')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],
                         'category with pk 4343434, does not exist')
