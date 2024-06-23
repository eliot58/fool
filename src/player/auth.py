from src.player.models import Player
from src.player.jwt_utils import decode_access_token
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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

async def get_userId(userId: int):
    return userId