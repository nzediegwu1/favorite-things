from rest_framework.test import APITestCase
from api.models import Category, AuditLog
from api.serializers import CategorySerializer


class TestCreateCategoryAuditLog(APITestCase):
    category = {}

    def setUp(self):
        new_category = {'name': 'Movies'}
        category = Category.objects.create(**new_category)
        self.category = CategorySerializer(category).data

    def test_audit_log_created_when_new_category_created(self):
        audit_log = AuditLog.objects.filter(model='category',
                                            resource_id=self.category['id'])
        self.assertEqual(len(audit_log), 1)
        [create_log] = audit_log
        self.assertEqual(create_log.before, {})
        self.assertEqual(create_log.after['name'], self.category['name'])
        self.assertEqual(create_log.action, 'create')

    def test_audit_log_created_when_category_updated(self):
        update = {'name': 'Action movies'}
        category_id = self.category['id']
        self.client.put(f'/categories/{category_id}', update, format='json')
        audit_log = AuditLog.objects.filter(model='category',
                                            resource_id=category_id)
        self.assertEqual(len(audit_log), 2)
        [_, update_log] = audit_log
        self.assertEqual(update_log.before, self.category)
        self.assertEqual(update_log.after['name'], update['name'])
        self.assertEqual(update_log.action, 'update')

    def test_audit_log_created_when_category_deleted(self):
        category_id = self.category['id']
        response = self.client.delete(f'/categories/{category_id}')
        self.assertEqual(response.status_code, 204)
        audit_log = AuditLog.objects.filter(model='category',
                                            resource_id=category_id)
        delete_log = list(audit_log)[-1]
        self.assertEqual(delete_log.after, {})
        self.assertEqual(delete_log.action, 'delete')
