from rest_framework.test import APITestCase
from api.models import Category


class TestDeleteCategory(APITestCase):
    def test_delete_category_succeeds_with_valid_id(self):
        fam = Category.objects.create(name='Family')
        response = self.client.delete(f'/categories/{fam.id}')
        self.assertEqual(response.status_code, 204)
        deleted_category = Category.objects.get(pk=fam.id)
        self.assertTrue(deleted_category.deleted)

    def test_delete_category_fails_with_invalid_id(self):
        response = self.client.delete('/categories/yaf')
        self.assertEqual(response.status_code, 404)

    def test_delete_category_fails_with_unexisting_id(self):
        response = self.client.delete('/categories/9999999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')
