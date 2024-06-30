from tortoise import fields, models
from .schemas import GameType, Currency

class Game(models.Model):
    id = fields.IntField(pk=True)
    bet = fields.IntField()
    currency = fields.CharEnumField(Currency)
    game_type = fields.CharEnumField(GameType)
    num_players = fields.IntField(default=0)
    host = fields.ForeignKeyField("models.Player", on_delete=fields.CASCADE)
    players = fields.ManyToManyField("models.GamePlayers")


class GamePlayers(models.Model):
    player = fields.ForeignKeyField("models.Player")
    is_done = fields.BooleanField(default=False)
    cards = fields.JSONField()