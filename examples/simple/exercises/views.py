from django.views.generic import ListView, TemplateView

from books.mixins import JSONResponseMixin
from books.models import Author, Book, Publisher

import factories

__all__ = (
    'AddAuthorsToBookView',
    'AuthorListView',
    'AuthorListJSONView',
    'BookListView',
    'CreateAuthorsView',
    'PublisherListView',
    'PublisherIDsView',
    'UpdateBooksView',
    'IndexView',
)


class IndexView(TemplateView):
    """Index."""

    template_name = 'exercises/index.html'


class BookListView(ListView):
    """Books.

    Optimise queries.
    """

    model = Book
    template_name = 'exercises/book_list.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all()


class AuthorListView(ListView):
    """Authors.

    Optimise queries.
    """

    model = Author
    template_name = 'exercises/author_list.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all()


class PublisherListView(ListView):
    """Publishers.

    Optimise code and queries.
    """

    model = Publisher
    template_name = 'exercises/publisher_list.html'

    def get_queryset(self):
        """Get queryset."""
        return self.model.objects.all()


class AuthorListJSONView(JSONResponseMixin, TemplateView):
    """Authors list JSON response.

    Optimise code and queries.
    """

    model = Author

    def get_data(self, context):
        """Get queryset."""
        return list(
            {
                'id': __o.id,
                'salutation': __o.salutation,
                'name': __o.name,
                'email': __o.email,
                'number_of_books': __o.books.count(),
            } for __o in self.model.objects.all()
        )

    def render_to_response(self, context, **response_kwargs):
        """Render."""
        response_kwargs.update({'safe': False})

        return self.render_to_json_response(context, **response_kwargs)


class CreateAuthorsView(TemplateView):
    """Create authors view.

    Optimise code and queries.
    """

    template_name = 'exercises/create_authors.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        authors_list = []
        for __i in range(1, 50):
            author = factories.AuthorFactory.build()
            author.save()
            authors_list.append(author)

        return {'object_list': authors_list}


class AddAuthorsToBookView(TemplateView):
    """Add authors to a book view.

    Optimise code and queries.
    """

    template_name = 'exercises/add_authors_to_book.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        book = Book.objects.select_related('publisher').first()

        authors = Author.objects.filter()[:50]

        for author in authors:
            book.authors.add(author)

        return {'object_list': [book], 'book_authors': authors}


class PublisherIDsView(TemplateView):
    """List of Publisher IDs."""

    template_name = 'exercises/publisher_ids.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        books = Book.objects.filter()[:50]

        publisher_ids = [__b.publisher.id for __b in books]

        return {'object_list': publisher_ids}


class UpdateBooksView(TemplateView):
    """Update books view.."""

    template_name = 'exercises/update_books.html'

    def get_context_data(self, **kwargs):
        """Get context data."""
        # Just get some book IDs
        book_ids = Book.objects.values_list('id', flat=True)[:50]

        books = Book.objects.filter(id__in=book_ids)

        for counter, book in enumerate(books):
            book.stock_count -= 1
            book.save()

        counter += 1  # Because our counter is zero-based

        return {'number_of_books_updated': counter}
