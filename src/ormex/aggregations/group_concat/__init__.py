from nine.versions import DJANGO_LTE_1_9

if DJANGO_LTE_1_9:
    from .django_lte_1_9 import *
else:
    from .django_gt_1_10 import *

__title__ = 'ormex.aggregations.group_concat'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
