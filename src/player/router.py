from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict, List, Union
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, WebSocketException, status
from .models import Player, Player_Pydantic
from .auth import check_telegram_authorization, get_current_player_with_token, get_current_player
from .jwt_utils import create_access_token

router = APIRouter(
    tags=["player"]
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.game_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, player: Player):
        await websocket.accept()
        self.active_connections[player.tg_id] = websocket
        player.is_online = True
        await player.save()

    async def disconnect(self, player: Player):
        if player.tg_id in self.active_connections:
            del self.active_connections[player.tg_id]
            player.is_online = False
            await player.save()

    async def send_personal_message(self, message: str, user_id: int):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def connect_to_game(self, game_id: int, websocket: WebSocket):
        if game_id not in self.game_connections:
            self.game_connections[game_id] = []
        await websocket.accept()
        self.game_connections[game_id].append(websocket)

    def disconnect_from_game(self, game_id: int, websocket: WebSocket):
        self.game_connections[game_id].remove(websocket)
        if not self.game_connections[game_id]:
            del self.game_connections[game_id]

    async def broadcast_to_game(self, game_id: int, message: str):
        if game_id in self.game_connections:
            for connection in self.game_connections[game_id]:
                await connection.send_text(message)

manager = ConnectionManager()

async def get_token(
    websocket: WebSocket,
    token: Annotated[Union[str, None], Query()] = None,
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token

@router.post("/token")
async def token(auth_data: dict):
    validated_data = check_telegram_authorization(auth_data)
    player = await Player.filter(tg_id=validated_data["id"])
    if not player:
        await Player.create(tg_id=validated_data["id"])
    token = create_access_token(str(validated_data["id"]))
    return {"access_token": token}



@router.post("/create-player/{tg_id}")
async def create_player(tg_id: int):
    await Player.create(tg_id=tg_id)
    return {"success": True}

# @router.get("/friends")
# async def get_friends(player: Player = Depends(get_current_player)):
#     return await player.friends.all()

@router.post("/claim/{tg_id}")
async def claim(tg_id: int):
    player = await Player.get(tg_id=tg_id)
    if player.last_claim + timedelta(hours=23) <= datetime.now(timezone.utc):
        player.foolcoin += 100
        player.last_claim = datetime.now(timezone.utc)
    await player.save()
    return player


@router.post("/friends/{id}/{friend_id}")
async def add_friends(id: int, friend_id: int):
    player = await Player.get(tg_id=id)
    friend = await Player.get(tg_id=friend_id)
    await player.friends.add(friend)
    await player.save()
    await friend.friends.add(player)
    await friend.save()
    return await player.friends.all()

@router.get("/friends/{tg_id}")
async def get_friends(tg_id: int):
    player = await Player.get(tg_id=tg_id)
    return await player.friends.all()

@router.websocket("/ws/global/{tg_id}")
async def websocket_global_endpoint(websocket: WebSocket, tg_id: int):
    player = await Player.get(tg_id=tg_id)
    await manager.connect(websocket)
    player_data = await Player_Pydantic.from_tortoise_orm(player)
    await manager.send_personal_message(player_data.model_dump_json(), player.tg_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{data}", player.tg_id)
    except WebSocketDisconnect:
        await manager.disconnect(player)

# @router.websocket("/ws/game/{game_id}")
# async def websocket_game_endpoint(websocket: WebSocket, game_id: int, token: Annotated[str, Depends(get_token)]):
#     await manager.connect_to_game(game_id, websocket)
#     await manager.send_personal_message()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast_to_game(game_id, f"User {player.tg_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect_from_game(game_id, websocket)
#         await manager.broadcast_to_game(game_id, f"User {player.tg_id} left the game chat")


