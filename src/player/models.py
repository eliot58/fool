from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Player(models.Model):
    tg_id = fields.BigIntField(pk=True)
    invited_by = fields.BigIntField(null=True)
    