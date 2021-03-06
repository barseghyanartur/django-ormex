"""
Base tests module.

- setup_app: Setup the app, collect the static, mark app setup as completed.
"""

from django.core.management import call_command

from .base import (
    is_app_setup_completed,
    mark_app_setup_as_completed,
)

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = ('setup_app',)


def setup_app(collectstatic=False):
    """Set up app."""
    if is_app_setup_completed():
        return False

    if collectstatic:
        call_command('collectstatic', verbosity=3, interactive=False)

    mark_app_setup_as_completed()
