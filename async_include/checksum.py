# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

import hashlib


def make(string):
    key = '{0}-{1}'.format(string, settings.SECRET_KEY)

    try:
        return hashlib.md5(key).hexdigest()
    except TypeError:
        return hashlib.md5(key.encode('utf-8')).hexdigest()
