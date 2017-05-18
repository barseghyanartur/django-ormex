from django.conf.urls import url

from .views import (
    AddAuthorsToBookView,
    AuthorListView,
    AuthorListJSONView,
    BookListView,
    CreateAuthorsView,
    PublisherListView,
    PublisherIDsView,
    UpdateBooksView,
    IndexView,
)

__all__ = ('urlpatterns',)


urlpatterns = [
    # Authors list
    url(r'^authors/$', AuthorListView.as_view(), name='exercises.authors'),

    # Books list
    url(r'^books/$', BookListView.as_view(), name='exercises.books'),

    # Publishers list
    url(r'^publishers/$',
        PublisherListView.as_view(),
        name='exercises.publishers'),

    # Publisher IDs
    url(r'^publisher-ids/$',
        PublisherIDsView.as_view(),
        name='exercises.publisher_ids'),

    # Authors list in JSON format
    url(r'^authors-json/$',
        AuthorListJSONView.as_view(),
        name='exercises.authors_json'),

    # Create authors view
    url(r'^create-authors/$',
        CreateAuthorsView.as_view(),
        name='exercises.create_authors'),

    # Add authors to a book view
    url(r'^add-authors-to-book/$',
        AddAuthorsToBookView.as_view(),
        name='exercises.add_authors_to_book'),

    # Update books view
    url(r'^update-books/$',
        UpdateBooksView.as_view(),
        name='exercises.update_books'),

    # Index view
    url(r'^$', IndexView.as_view(), name='exercises.index'),
]
