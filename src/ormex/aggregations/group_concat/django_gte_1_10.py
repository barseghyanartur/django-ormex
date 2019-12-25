import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Aggregate

from .base import GroupConcatMixin

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'GroupConcat',
    'MySQLGroupConcat',
    'PostgreSQL8GroupConcat',
    'PostgreSQL9GroupConcat',
    'PostgreSQLGroupConcat',
    'SQLiteGroupConcat',
)

LOGGER = logging.getLogger(__name__)


class MySQLGroupConcat(Aggregate, GroupConcatMixin):
    """SQL group concat.

    Works fine with SQLite and MySQL.
    """

    function = 'group_concat'

    @property
    def template(self):
        """SQL template."""
        separator = self.extra.get('separator')
        order_by_sql = self.get_order_by_sql()
        distinct_sql = self.get_distinct_sql()
        separator_sql = ' SEPARATOR "%(separator)s" ' if separator else ''

        sql = '%(function)s( '

        if distinct_sql:
            sql += distinct_sql

        sql += ' %(field)s '

        if separator_sql:
            sql += separator_sql

        if order_by_sql:
            sql += order_by_sql

        sql += ')'

        return sql

        # if separator:
        #     return '%(function)s(' \
        #            '%(field)s ' \
        #            'SEPARATOR "%(separator)s"' \
        #            ')'
        # else:
        #     return '%(function)s(' \
        #            '%(field)s' \
        #            ')'


class SQLiteGroupConcat(Aggregate, GroupConcatMixin):
    """SQLite group concat."""

    function = 'group_concat'

    @property
    def template(self):
        """SQL template."""
        separator = self.extra.get('separator')
        # order_by_sql = self.get_order_by_sql()
        distinct_sql = self.get_distinct_sql()
        separator_sql = ' , "%(separator)s" ' if separator else ''

        sql = '%(function)s( '

        if distinct_sql:
            sql += distinct_sql

        sql += ' %(field)s '

        if separator_sql:
            sql += separator_sql

        # if order_by_sql:
        #     sql += order_by_sql

        sql += ')'

        return sql


class PostgreSQL9GroupConcat(Aggregate, GroupConcatMixin):
    """PostgreSQL group concat.

    For PostgreSQL >= 9.0.
    """

    function = 'string_agg'

    def __init__(self, *expressions, **extra):
        # For PostgreSQL separator is an obligatory
        if 'separator' not in extra:
            extra.update({'separator': ', '})
        super(PostgreSQL9GroupConcat, self).__init__(*expressions, **extra)

    @property
    def template(self):
        # The ::text cast is a hardcoded hack to work with integer columns.
        # Also, separator is obligatory
        order_by_sql = self.get_order_by_sql()
        # distinct_sql = self.get_distinct_sql()

        sql = "%(function)s(" \
              "%(field)s::text, " \
              "'%(separator)s' "

        if order_by_sql:
            sql += order_by_sql

        sql += " )"

        return sql

        # if order_by:
        #     return "%(function)s(" \
        #            "%(field)s::text, " \
        #            "'%(separator)s' " \
        #            "ORDER BY %(order_by)s" \
        #            ")"
        # else:
        #     return "%(function)s(" \
        #            "%(field)s::text, " \
        #            "'%(separator)s'" \
        #            ")"


class PostgreSQL8GroupConcat(Aggregate, GroupConcatMixin):
    """PostgreSQL group concat.

    For PostgreSQL >= 8.4 and < 9.0.
    """

    function = 'array_to_string'

    def __init__(self, *expressions, **extra):
        # For PostgreSQL separator is an obligatory
        if 'separator' not in extra:
            extra.update({'separator': ', '})
        super(PostgreSQL9GroupConcat, self).__init__(*expressions, **extra)

    @property
    def template(self):
        order_by_sql = self.get_order_by_sql()
        # distinct_sql = self.get_distinct_sql()

        sql = "%(function)s(" \
              "array_agg(%(field)s), " \
              "'%(separator)s' "

        if order_by_sql:
            sql += order_by_sql

        sql += " )"

        return sql

        # if order_by:
        #     return "%(function)s(" \
        #            "array_agg(%(field)s), " \
        #            "'%(separator)s'" \
        #            "ORDER BY %(order_by)s" \
        #            ")"
        # else:
        #     return "%(function)s(" \
        #            "array_agg(%(field)s), " \
        #            "'%(separator)s'" \
        #            ")"


PostgreSQLGroupConcat = PostgreSQL9GroupConcat


def detect_group_concat_class():
    """Detect GroupConcat class."""
    engine = settings.DATABASES['default'].get('ENGINE', None)

    if not engine:
        raise ImproperlyConfigured("No DATABASES specified in settings.")

    if 'sqlite3' in engine:
        return SQLiteGroupConcat
    elif 'postgresql' in engine:
        return PostgreSQLGroupConcat
    elif 'mysql' in engine:
        return MySQLGroupConcat
    else:
        raise NotImplementedError(
            "Your database backend is not supported."
        )


GroupConcat = detect_group_concat_class()
