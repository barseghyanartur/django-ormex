class GroupConcatMixin(object):

    def get_distinct_sql(self):
        """Get distinct sql."""
        distinct = self.extra.get('distinct', None)
        return " DISTINCT " if distinct is True else ''

    def get_order_by_sql(self):
        """Get order_by sql."""
        order_by = self.extra.get('order_by', None)
        if order_by == 'self':
            return " ORDER BY %(field)s " if order_by is not None else ''
        else:
            return " ORDER BY %(order_by)s " if order_by is not None else ''
