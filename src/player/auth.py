from src.player.models import Player
from src.player.jwt_utils import decode_access_token
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.config.settings import BOT_TOKEN
import hashlib
import hmac
import time

security = HTTPBearer()

async def get_current_player(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_data = decode_access_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    tg_id = token_data.get("sub")
    player = await Player.get(tg_id=tg_id)
    return player


async def get_current_player_with_token(token: str):
    token_data = decode_access_token(token)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    tg_id = token_data.get("sub")
    player = await Player.get(tg_id=tg_id)
    return player

def check_telegram_authorization(auth_data):
    check_hash = auth_data['hash']
    auth_data.pop('hash')
    
    data_check_arr = []
    for key, value in auth_data.items():
        data_check_arr.append(f"{key}={value}")
    data_check_arr.sort()
    
    data_check_string = "\n".join(data_check_arr)
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if hash != check_hash:
        raise HTTPException(status_code=400, detail='Data is NOT from Telegram')
    
    if (time.time() - auth_data['auth_date']) > 86400:
        raise HTTPException(status_code=400, detail='Data is outdated')
    
    return auth_data