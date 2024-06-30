from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Player(models.Model):
    tg_id = fields.BigIntField(pk=True)
    cups = fields.IntField(default=0)
    foolcoin = fields.IntField(default=100)
    toncoin = fields.IntField(default=0)
    notcoin = fields.IntField(default=0)
    tether = fields.IntField(default=0)
    last_claim = fields.DatetimeField(auto_now_add=True)
    is_online = fields.BooleanField(default=True)
    is_free = fields.BooleanField(default=True)
    friends = fields.ManyToManyField('models.Player', related_name='friends_with')


Player_Pydantic = pydantic_model_creator(Player, name="Player")