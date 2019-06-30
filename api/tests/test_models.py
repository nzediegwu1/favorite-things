from django.test import TestCase
from ..models import Category, Favourite

banga_soup = {
    'title': 'Banga Soup',
    'description': 'Best delicacy from southern Nigeria',
    'ranking': 1
}


class ModelTests(TestCase):
    def setUp(self):
        food = Category.objects.create(name='food')
        Favourite.objects.create(**banga_soup, category=food)

    def test_category(self):
        category = Category.objects.get(name='food')
        self.assertEqual(category.name, 'food')
        self.assertEqual(category.get_count(), 1)

    def test_categoery_instance(self):
        self.assertEqual(Category(name='books').__str__(), 'books')

    def test_favourite(self):
        favourite = Favourite.objects.get(title=banga_soup['title'])
        self.assertEqual(favourite.title, banga_soup['title'])
        self.assertEqual(favourite.deleted, False)
        print(favourite.created_date)
        print(favourite.modified_date)

    def test_favourite_instance(self):
        favourite = Favourite(**banga_soup, category=Category(name='books'))
        self.assertEqual(favourite.__str__(), banga_soup['title'])
