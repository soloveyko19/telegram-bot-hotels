""" Модуль с моделями базы данных "telegram_bot.db" """


from peewee import Model, SqliteDatabase, CharField, DateTimeField, BigIntegerField
from datetime import datetime as dt
import os


path = os.path.abspath(os.path.join('database', 'telegram_bot.db'))
db = SqliteDatabase(path)


class BaseModel(Model):
    """ Класс шаблон определяющий базу данных для классов наследников. Родительский класс Model. """
    class Meta:
        database = db


class Hotel(BaseModel):
    """
    Класс модели Hotel. Родительский класс BaseModel.

    Модель для хранения истории поиска отелей.

    Attributes:
        hotel_name (CharField): название отеля
        added_at (DateTimeField): время добавления записи
        user_id (BigIntegerField): Телеграм id пользователя
        command (CharField): Команда с которой был найден отель
    """
    hotel_name = CharField(null=False, max_length=30)
    added_at = DateTimeField(default=dt.now)
    user_id = BigIntegerField(null=None)
    command = CharField(null=False, max_length=6)


with db:
    if not Hotel.table_exists():
        Hotel.create_table()
