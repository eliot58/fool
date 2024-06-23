from datetime import datetime, timedelta, timezone
from src.config.settings import SECRET_AUTH
import jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(tg_id: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": tg_id, "exp": expire}
    token = jwt.encode(payload, SECRET_AUTH, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str):
    try:
        decoded_payload = jwt.decode(token, SECRET_AUTH, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return "Signature has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"