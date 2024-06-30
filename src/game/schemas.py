from enum import Enum
from pydantic import BaseModel

class GameType(Enum):
    flip_up = "flip_up"
    translated = "translated"


class Currency(Enum):
    toncoin = "toncoin"
    notcoin = "notcoin"
    tether = "tether"
    foolcoin = "foolcoin"


class CreateGame(BaseModel):
    bet: int
    currency: Currency
    game_type: GameType
    num_players: int
    

