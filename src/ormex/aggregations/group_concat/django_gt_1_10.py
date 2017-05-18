from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Aggregate

__title__ = 'ormex.aggregations.group_concat.django_gt_1_10'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'GroupConcat',
    'MySQLGroupConcat',
    'PostgreSQL8GroupConcat',
    'PostgreSQL9GroupConcat',
    'PostgreSQLGroupConcat',
    'SQLiteGroupConcat',
)


class MySQLGroupConcat(Aggregate):
    """SQL group concat.

    Works fine with SQLite and MySQL.
    """

    function = 'group_concat'

    @property
    def template(self):
        """SQL template."""
        separator = self.extra.get('separator')
        if separator:
            return '%(function)s(%(field)s, "%(separator)s")'
        else:
            return '%(function)s(%(field)s)'


class SQLiteGroupConcat(MySQLGroupConcat):
    """SQLite group concat.

    Works just the same way as MySQLConcat.
    """


class PostgreSQL9GroupConcat(Aggregate):
    """PostgreSQL group concat.

    For PostgreSQL >= 9.0.
    """

    sql_function = 'string_agg'

    @property
    def template(self):
        # The ::text cast is a hardcoded hack to work with integer columns
        return "%(function)s(%(field)s::text, '%(separator)s')"


class PostgreSQL8GroupConcat(Aggregate):
    """PostgreSQL group concat.

    For PostgreSQL >= 8.4 and < 9.0.
    """

    function = 'array_to_string'

    @property
    def template(self):
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


GroupConcat = detect_group_concat_class()
