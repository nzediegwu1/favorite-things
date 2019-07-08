from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone


def min_length(field, length):
    return f'{field} should not be less than {length}'


alphabet_only = RegexValidator(r'^[a-zA-Z \']*$',
                               'Should contain only alphabets')


class Category(models.Model):
    """
    Defines the properties of a Category.
    A category can have multiple favourites
    """
    name = models.CharField(max_length=30,
                            unique=True,
                            validators=[alphabet_only])

    @property
    def count(self):
        return self.favourites.filter(deleted=False).count()

    def __str__(self):
        return self.name


class Favourite(models.Model):
    """
    Defines the porperties of a Favourite
    A Favourite belongs to one category
    """
    title = models.CharField(max_length=60, validators=[alphabet_only])
    description = models.TextField(
        validators=[MinLengthValidator(10, min_length('description', 10))])
    ranking = models.IntegerField()
    deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    modified_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='favourites')

    def __str__(self):
        return self.title
