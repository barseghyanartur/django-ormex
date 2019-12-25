from nine.versions import DJANGO_LTE_1_9

if DJANGO_LTE_1_9:
    from .django_lte_1_9 import *
else:
    from .django_gte_1_10 import *

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
