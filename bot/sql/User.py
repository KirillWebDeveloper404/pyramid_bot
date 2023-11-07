from enum import unique
from .BaseModel import BaseModel
from peewee import *


class User(BaseModel):
    tg_id = TextField()

    class Meta:
        table_name = 'panel_user'


class Messages(BaseModel):
    address = TextField()
    text = TextField()

    class Meta:
        table_name = "panel_messages"
