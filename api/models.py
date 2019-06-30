from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


def min_length(field, length):
    return f'{field} should not be less than {length}'


class Category(models.Model):
    """
    Defines the properties of a Category.
    A category can have multiple favourites
    """
    name = models.CharField(max_length=30, unique=True)

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
    title = models.CharField(max_length=60)
    description = models.TextField(
        validators=[MinLengthValidator(10, min_length('description', 10))])
    ranking = models.IntegerField()
    deleted = models.BooleanField(default=False)
    # created_date should be generated upon creation but skipped upon update/delete
    # add date validation to created_date
    created_date = models.DateTimeField(null=True)
    modified_date = models.DateTimeField(null=True, default=timezone.now)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='favourites')

    def __str__(self):
        return self.title
