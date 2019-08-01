from rest_framework.test import APITestCase
from api.models import Category, AuditLog, Favourite
from api.serializers import FavouriteSerializer
from api.tests.mocks import jellof_rice, jellof_rice_update


class TestCreateFavouriteAuditLog(APITestCase):
    category_id = 0
    favourite = {}

    def setUp(self):
        new_category = Category.objects.create(name='food')
        new_favourite = Favourite.objects.create(**jellof_rice(new_category))
        self.category_id = new_category.id
        self.favourite = FavouriteSerializer(new_favourite).data

    def test_audit_log_created_when_new_favourite_created(self):
        audit_log = AuditLog.objects.filter(model='favourite',
                                            resource_id=self.favourite['id'])
        self.assertEqual(len(audit_log), 1)
        [create_log] = audit_log
        self.assertEqual(create_log.before, {})
        self.assertEqual(create_log.after['title'], self.favourite['title'])
        self.assertEqual(create_log.action, 'create')

    def test_audit_log_created_when_favourite_updated(self):
        update = jellof_rice_update(self.category_id)
        favourite_id = self.favourite['id']
        self.client.put(f'/favourites/{favourite_id}', update, format='json')
        audit_log = AuditLog.objects.filter(model='favourite',
                                            resource_id=favourite_id)
        self.assertEqual(len(audit_log), 2)
        [_, update_log] = audit_log
        self.assertEqual(update_log.before['description'],
                         self.favourite['description'])
        self.assertEqual(update_log.after['description'],
                         update['description'])
        self.assertEqual(update_log.action, 'update')

    def test_audit_log_created_when_favourite_deleted(self):
        favourite_id = self.favourite['id']
        response = self.client.delete(f'/favourites/{favourite_id}')
        self.assertEqual(response.status_code, 204)
        audit_log = AuditLog.objects.filter(model='favourite',
                                            resource_id=favourite_id)
        delete_log = list(audit_log)[-1]
        self.assertEqual(delete_log.after, {})
        self.assertEqual(delete_log.action, 'delete')
