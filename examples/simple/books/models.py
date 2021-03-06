from django.conf import settings
from django.db import models
from django.utils.translation import gettext

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

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    website = models.URLField(max_length=255)

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Author(models.Model):
    """Author."""

    salutation = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    headshot = models.ImageField(upload_to='authors', null=True, blank=True)

    class Meta(object):
        """Meta options."""

        ordering = ["name"]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    """Book."""

    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('books.Author',
                                     related_name='books')
    publisher = models.ForeignKey(Publisher,
                                  related_name='books',
                                  on_delete=models.SET_NULL)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=255, unique=True)
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

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL)
    lines = models.ManyToManyField("books.OrderLine", blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta(object):
        """Meta options."""

        ordering = ["-created"]

    def __str__(self):
        return gettext('Order')


@python_2_unicode_compatible
class OrderLine(models.Model):
    """Order line."""

    book = models.ForeignKey('books.Book',
                             related_name='order_lines',
                             on_delete=models.SET_NULL)

    class Meta(object):
        """Meta options."""

        ordering = ["order__created"]

    def __str__(self):
        return gettext('{}').format(self.book.isbn)
