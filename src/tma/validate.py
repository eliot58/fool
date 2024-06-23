from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs
from src.tma.sign import sign
from src.tma.errors import UnexpectedFormatError, ExpiredError, SignMissingError, SignInvalidError


def validate(init_data, token, exp_in):
    try:
        q = parse_qs(init_data)
    except Exception:
        raise UnexpectedFormatError

    auth_date = None
    hash_value = None
    pairs = []

    for k, v in q.items():
        if k == 'hash':
            hash_value = v[0]
            continue
        elif k == 'auth_date':
            auth_date = datetime.fromtimestamp(int(v[0]))
        pairs.append(f"{k}={v[0]}")

    if not hash_value:
        raise SignMissingError

    if exp_in > 0 and auth_date:
        if auth_date + timedelta(seconds=exp_in) < datetime.now(timezone.utc):
            raise ExpiredError
        
    pairs = sorted(pairs)

    if sign('\n'.join(pairs), token) != hash_value:
        raise SignInvalidError

    return True