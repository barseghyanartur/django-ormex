from django.conf import settings
from django.db.models import Aggregate
from django.db.models.sql.aggregates import Aggregate as SQLAggregate
from django.core.exceptions import ImproperlyConfigured

from .base import GroupConcatMixin

__title__ = 'ormex.aggregations.group_concat.django_lte_1_9'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'GROUP_CONCAT_CLASS',
    'GroupConcat',
    'MySQLGroupConcat',
    'PostgreSQL8GroupConcat',
    'PostgreSQL9GroupConcat',
    'PostgreSQLGroupConcat',
    'SQLiteGroupConcat',
)


class MySQLGroupConcat(SQLAggregate, GroupConcatMixin):
    """SQL group concat.

    Works fine with SQLite and MySQL.
    """

    sql_function = 'group_concat'

    @property
    def sql_template(self):
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


class SQLiteGroupConcat(SQLAggregate, GroupConcatMixin):
    """SQLite group concat."""

    sql_function = 'group_concat'

    @property
    def sql_template(self):
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


class PostgreSQL9GroupConcat(SQLAggregate, GroupConcatMixin):
    """PostgreSQL group concat.

    For PostgreSQL >= 9.0.
    """

    sql_function = 'string_agg'

    def __init__(self, *expressions, **extra):
        # For PostgreSQL separator is an obligatory
        if 'separator' not in extra:
            extra.update({'separator': ', '})
        super(PostgreSQL9GroupConcat, self).__init__(*expressions, **extra)

    @property
    def sql_template(self):
        # The ::text cast is a hardcoded hack to work with integer columns.
        # Also, separator is obligatory
        order_by = self.extra.get('order_by', None)

        if order_by:
            return "%(function)s(" \
                   "%(field)s::text, " \
                   "'%(separator)s' " \
                   "ORDER BY %(order_by)s" \
                   ")"
        else:
            return "%(function)s(%(field)s::text, '%(separator)s')"


class PostgreSQL8GroupConcat(SQLAggregate, GroupConcatMixin):
    """PostgreSQL group concat.

    For PostgreSQL >= 8.4 and < 9.0.
    """

    sql_function = 'array_to_string'

    def __init__(self, *expressions, **extra):
        # For PostgreSQL separator is an obligatory
        if 'separator' not in extra:
            extra.update({'separator': ', '})
        super(PostgreSQL9GroupConcat, self).__init__(*expressions, **extra)

    @property
    def sql_template(self):
        order_by = self.extra.get('order_by', None)
        if order_by:
            return "%(function)s(" \
                   "array_agg(%(field)s), " \
                   "'%(separator)s'" \
                   "ORDER BY %(order_by)s" \
                   ")"
        else:
            return "%(function)s(array_agg(%(field)s), '%(separator)s')"


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


GROUP_CONCAT_CLASS = detect_group_concat_class()


class GroupConcat(Aggregate):
    """Group concat.

    Usage example:

    >>> .annotate(values=GroupConcat('value', separator=','))
    """

    def add_to_query(self, query, alias, col, source, is_summary):
        """Add to query."""
        aggregate = GROUP_CONCAT_CLASS(
            col,
            source=source,
            is_summary=is_summary,
            **self.extra
        )
        query.aggregates[alias] = aggregate
