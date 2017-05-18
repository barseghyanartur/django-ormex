============
django-ormex
============
Django ORM extensions.

Prerequisites
=============
- Django 1.8, 1.9, 1.10, 1.11
- Python 2.7, 3.4, 3.5, 3.6

Installation
============
(1) Install in your virtual environment.

    Latest stable version from PyPI:

    .. code-block:: sh

        pip install django-ormex

    Latest stable version from GitHub:

    .. code-block:: sh

        pip install https://github.com/barseghyanartur/django-ormex/archive/stable.tar.gz

Usage
=====
Common usage examples.

Aggregations
------------
Contains various modules for aggregations.

GroupConcat
~~~~~~~~~~~
Works like Concat, but for concatenating field values of related ManyToMany
model. For instance, you may use it if you have an ``Author`` model as
ManyToMany relation in the ``Book`` model
(``Book.authors = ManyToManyField(Author)``) and you want to have concatenated
list of all authors coupled to a given book.

Given the following models:

.. code-block:: python

    class Publisher(models.Model):
        """Publisher."""

        name = models.CharField(max_length=30)
        address = models.CharField(max_length=50)
        city = models.CharField(max_length=60)
        state_province = models.CharField(max_length=30)
        country = models.CharField(max_length=50)
        website = models.URLField()


    class Author(models.Model):
        """Author."""

        salutation = models.CharField(max_length=10)
        name = models.CharField(max_length=200)
        email = models.EmailField()
        headshot = models.ImageField(upload_to='authors', null=True, blank=True)


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

We could use GroupConcat as follows:

.. code-block:: python

    from ormex.aggregations import GroupConcat

    books = Book.objects.all() \
            .values('id',
                    'title',
                    'pages',
                    'price',
                    'publisher__id',
                    'publisher__name') \
            .annotate(
                authors__name=GroupConcat('authors__name', separator=', ')
            ) \
            .distinct()

Demo
====
Run demo locally
----------------
In order to be able to quickly evaluate the `django-ormex`, a demo
app (with a quick installer) has been created (works on Ubuntu/Debian, may
work on other Linux systems as well, although not guaranteed). Follow the
instructions below to have the demo running within a minute.

Grab the latest ``ormex_demo_installer.sh``:

.. code-block:: sh

    wget -O - https://raw.github.com/barseghyanartur/django-ormex/stable/examples/ormex_demo_installer.sh | bash

Open your browser and test the app.

- URL: http://127.0.0.1:8001/

If quick installer doesn't work for you, see the manual steps on running the
`example project
<https://github.com/barseghyanartur/django-ormex/tree/stable/examples>`_.

Testing
=======
Simply type:

.. code-block:: sh

    ./runtests.py

or use tox:

.. code-block:: sh

    tox

or use tox to check specific env:

.. code-block:: sh

    tox -e py35

or run Django tests:

.. code-block:: sh

    ./manage.py test ormex --settings=settings.testing

License
=======
GPL 2.0/LGPL 2.1

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
