from django.conf import settings
from django.db import models
from django.utils.translation import ugettext

from six import python_2_unicode_compatible

__all__ = (
    'Author',
    'Book',
    'Order',
    'OrderLine',
    'Publisher',
)


@python_2_unicode_compatible
class Publisher(models.Model):
    """Publisher."""

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta(object):
        """Meta options."""

        ordering = ["name"]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Author(models.Model):
    """Author."""

    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='authors', null=True, blank=True)

    class Meta(object):
        """Meta options."""

        ordering = ["name"]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    """Book."""

    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('books.Author', related_name='books')
    publisher = models.ForeignKey(Publisher, related_name='books')
    publication_date = models.DateField()
    isbn = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(default=200)
    stock_count = models.PositiveIntegerField(default=30)

    class Meta(object):
        """Meta options."""

        ordering = ["isbn"]

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Order(models.Model):
    """Order."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    lines = models.ManyToManyField("books.OrderLine", blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta(object):
        """Meta options."""

        ordering = ["-created"]

    def __str__(self):
        return ugettext('Order')


@python_2_unicode_compatible
class OrderLine(models.Model):
    """Order line."""

    book = models.ForeignKey('books.Book', related_name='order_lines')

    class Meta(object):
        """Meta options."""

        ordering = ["order__created"]

    def __str__(self):
        return ugettext('{}').format(self.book.isbn)
