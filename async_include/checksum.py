import hashlib
import hmac
from django.conf import settings


def make(string: str) -> str:
    key = settings.SECRET_KEY.encode('utf-8')
    return hmac.new(key, string.encode('utf-8'), hashlib.sha256).hexdigest()
