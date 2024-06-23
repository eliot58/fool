import hmac
import hashlib
from urllib.parse import parse_qs


def sign(payload, key):
    sk_hmac = hmac.new(b'WebAppData', key.encode(), hashlib.sha256)
    imp_hmac = hmac.new(sk_hmac.digest(), payload.encode(), hashlib.sha256)
    return imp_hmac.hexdigest()


def sign_query_string(qs, key, auth_date):
    q = parse_qs(qs)
    payload = {k: v[0] for k, v in q.items() if k != 'hash' and k != 'auth_date'}
    payload['auth_date'] = str(int(auth_date.timestamp()))

    sorted_payload = '\n'.join(f"{k}={v}" for k, v in sorted(payload.items()))
    return sign(sorted_payload, key)