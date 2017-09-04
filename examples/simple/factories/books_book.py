import random

from factory import (
    DjangoModelFactory,
    SubFactory,
    post_generation,
    LazyAttribute
)

from books.models import Book

from .factory_faker import Faker
from .books_author import (
    # AuthorFactory,
    LimitedAuthorFactory,
    SingleAuthorFactory,
)
from .books_order import OrderFactory
from .books_orderline import OrderLineFactory

__all__ = (
    'BookFactory',
    'BookWithUniqueTitleFactory',
    'SingleBookFactory',
)


class BaseBookFactory(DjangoModelFactory):
    """Base book factory."""

    title = Faker('text', max_nb_chars=100)
    publisher = SubFactory('factories.books_publisher.LimitedPublisherFactory')
    publication_date = Faker('date')
    price = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    isbn = Faker('pystr', min_chars=10, max_chars=10)
    pages = LazyAttribute(
        lambda __x: random.randint(10, 200)
    )

    class Meta(object):
        """Meta class."""

        model = Book
        abstract = True

    @post_generation
    def authors(obj, created, extracted, **kwargs):
        """Create `Author` objects for the created `Book` instance."""
        if created:
            # Create random amount of `Author` objects.
            amount = random.randint(3, 7)
            authors = LimitedAuthorFactory.create_batch(amount, **kwargs)
            obj.authors.add(*authors)

    @post_generation
    def orders(obj, created, extracted, **kwargs):
        """Create `Order` objects for the created `Book` instance."""
        if created:
            # Create 3 `Order` objects.
            amount = random.randint(2, 7)
            orders = OrderFactory.create_batch(amount, **kwargs)
            order_line_kwargs = dict(kwargs)
            order_line_kwargs['book'] = obj
            for order in orders:
                # Create 1 `OrderLine` object.
                amount = random.randint(1, 5)
                order_lines = OrderLineFactory.create_batch(
                    amount, **order_line_kwargs
                )
                order.lines.add(*order_lines)


class BookFactory(BaseBookFactory):
    """Book factory."""


class BookWithUniqueTitleFactory(BaseBookFactory):
    """Book factory with unique title attribute."""

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('title',)


class SingleBookFactory(BaseBookFactory):
    """Book factory, but limited to a single book."""

    id = 999999
    title = "Django performance unchained"
    publisher = SubFactory('factories.books_publisher.SinglePublisherFactory')

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)

    @post_generation
    def authors(obj, created, extracted, **kwargs):
        """Create `Author` objects for the created `Book` instance."""
        if created:
            # Create a single `Author` object.
            author = SingleAuthorFactory()
            obj.authors.add(author)
