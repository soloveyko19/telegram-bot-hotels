""" Модуль подгрузки всех элементов бота """


from telebot import TeleBot
from config_data import config
from telebot.storage import StateMemoryStorage
from telebot.custom_filters import StateFilter, IsDigitFilter


state_storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(IsDigitFilter())

