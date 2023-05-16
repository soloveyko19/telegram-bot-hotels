""" Модуль команды /history """


from loader import bot
from telebot.types import Message
from database.db_functions import get_hotels_history


@bot.message_handler(commands=['history'], state=None)
def send_history(message: Message):
    """ Функция вывода последних 10 запросов пользователя """
    hotels = get_hotels_history(message.from_user.id)
    if hotels:
        history = str()
        for number, i_hotel in enumerate(hotels):
            history += f'{number + 1}. {i_hotel[0]}, команда {i_hotel[1]}\n'
        bot.send_message(message.chat.id,
                         f'История запросов отелей:\n'
                         f'{history}')
    else:
        bot.send_message(message.from_user.id,
                         'Ваша история запросов пуста :)')
