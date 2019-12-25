# -*- coding: utf-8 -*-
"""
Test the aggregations package.
"""

import unittest

from django.apps import apps
from django.core.management import call_command
from django.test import Client, TestCase

import pytest

from ..aggregations import GroupConcat

from .base import log_info
from .helpers import setup_app

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('OrmexAggregationsTest',)


@pytest.mark.django_db
class OrmexAggregationsTest(TestCase):
    """Testing `django-ormex` aggregations functionality."""

    pytestmark = pytest.mark.django_db

    def setUp(self):
        """Set up."""
        setup_app()
        self.client = Client()
        call_command(
            'books_create_test_data',
            number=5
        )

    @log_info
    def __test_group_concat(self, **kwargs):
        """Test ``GroupConcat``."""
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
            .annotate(authors__name=GroupConcat('authors__name', **kwargs)) \
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

    @log_info
    def test_01_group_concat(self):
        """Test GroupConcat."""
        self.__test_group_concat()

    @log_info
    def test_02_group_concat_with_separator(self):
        """Test GroupConcat."""
        self.__test_group_concat(separator=',')

    @log_info
    def test_03_group_concat_with_alternative_separator(self):
        """Test GroupConcat."""
        self.__test_group_concat(separator='|')

    @log_info
    def test_04_group_concat_with_order_by(self):
        """Test GroupConcat."""
        self.__test_group_concat(order_by='self')


if __name__ == '__main__':
    unittest.main()
