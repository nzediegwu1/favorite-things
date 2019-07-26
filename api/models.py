from django.db import models
from django.shortcuts import get_object_or_404
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone


def min_length(field, length):
    return f'{field} should not be less than {length}'


alphabet_only = RegexValidator(r'^[a-zA-Z \']*$',
                               'Should contain only alphabets')


class BaseModel():
    @classmethod
    def soft_delete(cls, pk):
        """Soft-deletes a record in database

        Args:
            model(cls): model of the entity to delete 
            pk(number): id of the record to delete
        Returns:
            None
        """
        item = get_object_or_404(cls, pk=pk, deleted=False)
        item.deleted = True
        item.save()


class Category(models.Model, BaseModel):
    """
    Defines the properties of a Category.
    A category can have multiple favourites
    """
    name = models.CharField(max_length=30,
                            unique=True,
                            validators=[alphabet_only])
    deleted = models.BooleanField(default=False)

    @property
    def count(self):
        return self.favourites.filter(deleted=False).count()

    def __str__(self):
        return self.name


class Favourite(models.Model, BaseModel):
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


class MetaData(models.Model):
    """
    Defines the properties of Metadata associated to favourites
    Each metadata belongs to a favourite, a favourite can have many metadata
    """
    DATA_TYPES = (('text', 'Text'), ('number', 'Number'), ('date', 'Date'),
                  ('enum', 'Enum'))
    name = models.CharField(max_length=30, validators=[alphabet_only])
    data_type = models.CharField(max_length=10, choices=DATA_TYPES)
    value = models.CharField(max_length=100)
    favourite = models.ForeignKey(Favourite,
                                  on_delete=models.CASCADE,
                                  related_name='metadata')

    def __str__(self):
        return self.name
