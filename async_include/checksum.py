from django.conf import settings

import hashlib


def make(string: str) -> str:
    key = '{0}-{1}'.format(string, settings.SECRET_KEY)
    return hashlib.md5(key.encode('utf-8')).hexdigest()
