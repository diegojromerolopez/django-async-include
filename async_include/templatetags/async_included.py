# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.db import connection
from django.db.models.query import RawQuerySet
from django import template
from django.template.defaultfilters import length as django_length


register = template.Library()


# Replacement of length filter for RawQuerySets
@register.filter(is_safe=True)
def length(queryset):

    # If the queryset is a RawQuerySet,
    # we have to compute the COUNT on a different way
    if type(queryset) == RawQuerySet:

        # Preparing quote of the parameters
        def quote_param(param):
            if isinstance(param, ("".__class__, u"".__class__)):
                return "'{0}'".format(param)
            return param

        # For each parameter that needs it we have to quote it
        # (Django internally relies on the database system)
        quoted_params = [quote_param(param_i) for param_i in queryset.params]
        raw_query_sql = queryset.query.sql % (tuple(quoted_params))
        count_sql = (
            'SELECT COUNT(*) FROM ({0}) RAWQUERY;'.format(raw_query_sql)
        )

        # Execution of the code
        cursor = connection.cursor()
        cursor.execute(count_sql)
        row = cursor.fetchone()
        return row[0]

    # If the argument has any other type we use the standard length filter
    return django_length(queryset)
