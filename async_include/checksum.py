# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

import hashlib


def make(string):
    return hashlib.md5("{0}-{1}".format(string, settings.SECRET_KEY)).hexdigest()