from typing import Annotated, List
from fastapi import APIRouter, Body, Depends, HTTPException
from tortoise.exceptions import DoesNotExist
from .models import Player, Player_Pydantic, Inventory
from src.store.models import *
from .auth import get_userId, get_current_player
from .schemas import *
from tortoise.expressions import Q
from datetime import datetime, timedelta, timezone
from src.config.constant import more_exp_arr, level_up_exp, level_up_prize
from .jwt_utils import create_access_token
import random
import math

router = APIRouter(
    tags=["player"]
)