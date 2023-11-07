from peewee import Model, SqliteDatabase
from data.config import BASE_DIR

db = SqliteDatabase(BASE_DIR / '../bot.db')

class BaseModel(Model):

    class Meta:
        database = db