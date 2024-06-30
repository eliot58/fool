from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist
from .schemas import *
from .models import Game
from src.player.models import Player
from tortoise.expressions import Q
from datetime import datetime, timedelta, timezone

router = APIRouter(
    tags=["game"]
)

@router.post("/create-game/{tg_id}")
async def create_game(tg_id: int, game: CreateGame):
    player = await Player.get(tg_id=tg_id)
    game = await Game.create(host=player, **game.model_dump())
    return game