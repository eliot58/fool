import json
from urllib.parse import parse_qs
from src.tma.init_data import InitData
from src.tma.errors import UnexpectedFormatError


def parse(init_data):
    try:
        q = parse_qs(init_data)
    except Exception:
        raise UnexpectedFormatError

    pairs = {k: v[0] for k, v in q.items()}
    json_data = json.dumps(pairs)

    try:
        data = json.loads(json_data, object_hook=lambda d: InitData(**d))
    except Exception:
        raise UnexpectedFormatError

    return data
