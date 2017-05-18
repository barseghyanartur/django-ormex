# -*- coding: utf-8 -*-
"""
Test the core package.

- DummyThumbnailsCoreTest: Test core functionality.
"""

import unittest

from django.core.management import call_command
from django.test import Client, TestCase
from django.apps import apps

from ..aggregations import GroupConcat

from .base import log_info
from .helpers import setup_app

__title__ = 'ormex.tests.test_aggregations'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('OrmexAggregationsTest',)


class OrmexAggregationsTest(TestCase):
    """Testing `django-ormex` aggregations functionality."""

    def setUp(self):
        """Set up."""
        setup_app()
        self.client = Client()
        call_command(
            'books_create_test_data',
            number=5
        )

    @log_info
    def test_01_group_concat(self):
        """Test ``get_random_image``."""
        book_cls = apps.get_model('books', 'Book')
        book = book_cls.objects.all() \
            .select_related('publisher') \
            .prefetch_related('authors') \
            .only('id',
                  'title',
                  'pages',
                  'price',
                  'publisher__id',
                  'publisher__name',
                  'authors__id',
                  'authors__name') \
            .values('id',
                    'title',
                    'pages',
                    'price',
                    'publisher__id',
                    'publisher__name') \
            .annotate(authors__name=GroupConcat('authors__name')) \
            .distinct() \
            .last()

        self.assertIsNotNone(book['authors__name'])

        book_ = book_cls.objects.all() \
            .select_related('publisher') \
            .prefetch_related('authors') \
            .only('id',
                  'title',
                  'pages',
                  'price',
                  'publisher__id',
                  'publisher__name',
                  'authors__id',
                  'authors__name') \
            .last()

        for book_author in book_.authors.all():
            self.assertIn(book_author.name, book['authors__name'])

        return book['authors__name']

if __name__ == '__main__':
    unittest.main()
