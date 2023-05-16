""" Модуль отвечающий за команду /low """


from telebot.types import Message, CallbackQuery
from keyboards.inline.keyboard_by_dict import keyboard1
from loader import bot
from states.states import LowStates, AllStates
from utils.misc.api_requests import get_city, get_hotels


@bot.message_handler(commands=['low'], state=None)
def low_start(message: Message) -> None:
    """
    Функция начала опроса по комманде /low

    Присваивает пользователю начальное состояние для поиска города

    Args:
        message (Message): сообщение пользователя
    """
    bot.set_state(message.from_user.id, LowStates.city, message.chat.id)
    bot.send_message(message.chat.id,
                     'Отлично, будем искать самые дешевые отели!\n'
                     'Теперь введи с клавиатуры название города в котором будем искать отели.\n')


@bot.message_handler(state=LowStates.city)
def get_city_info(message: Message) -> None:
    """
    Функцияя вывода найденных городов из функции get_city.

    Если найденных городов больше одного то выводится inline клавиатура надписью на которой является имя города,
    а параметром callback является id этого города.
    Если найденный город только один, то сразу присваивается в хранилище id этого города и следущее состояние
    пользователю (HighStates.hotel).
    В случае если ни один город не найден то выводится соответсвуещее сообщение.

    Args:
        message (Message): сообщение пользователя
    """
    bot.send_message(message.chat.id,
                     f'Принято, ищу город {message.text.capitalize()}')
    cities = get_city(message.text)
    if len(cities) > 1:
        bot.send_message(message.chat.id,
                         'Уточните пожалуйста',
                         reply_markup=keyboard1(cities, back=True))
    elif len(cities) == 1:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city_id'] = cities.popitem()[1]
        bot.send_message(message.from_user.id,
                         f'Хорошо, давай дальше.\n'
                         'Введи количество отелей для вывода\n'
                         '(от 1 до 10 включительно)')
        bot.set_state(message.from_user.id, LowStates.hotel, message.chat.id)
    else:
        bot.send_message(message.chat.id,
                         f'Город {message.text.capitalize()} не найден.\n'
                         f'Убедитесь что ввели город правильно и попробуйте еще раз',
                         reply_markup=keyboard1(back=True))


@bot.message_handler(state=LowStates.hotel)
def chose_hotels_amount(message: Message) -> None:
    """
    Функция поиска отеля по данным введенные пользователем ранее

    Проверяет что число отелей которое ввел пользователь больше 0 но не более 10
    Если все условия проходят то пользователю выдается клавиатура с названием отелей, значением callback которых
    является id этого отеля.

    Args:
        message (Message): сообщение пользователя (кол-во отелей для вывода)
    """
    try:
        amt = int(message.text)
        if amt > 10:
            bot.send_message(message.chat.id,
                             'Выбрано слишком много отелей, пожалуйста введи число от 1 до 10')
        elif amt < 1:
            bot.send_message(message.chat.id,
                             'Выбрано слишком мало отелей, пожалуйста введи число от 1 до 10')
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotels_amt'] = amt
                bot.send_message(message.chat.id, 'Поиск отелей...')
                result = get_hotels(data['city_id'], data['hotels_amt'], "PRICE_LOW_TO_HIGH")
                if result:
                    bot.send_message(message.chat.id, 'Выберите отель', reply_markup=keyboard1(result, back=True))
                else:
                    bot.send_message(message.chat.id,
                                     'К сожалению в этом городе отелей не найдено.\n'
                                     'Вы вернулись в главное меню! /help')
                    bot.delete_state(message.from_user.id, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста введите целое число от 1 до 10')


@bot.callback_query_handler(func=lambda call: True, state=LowStates.city)
def city_id_chose(call: CallbackQuery) -> None:
    """
    Функция которая принимает все Callback если пользовательь находится в состоянии LowStates.city

    Присваивает данные Callback (id города) в хранилище пользователя

    Args:
        call (CallbackQuery): id города
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['city_id'] = call.data
    bot.send_message(call.message.chat.id, 'Хорошо, давай дальше\n'
                                           'Введи количество отелей для вывода\n'
                                           '(от 1 до 10 включительно)')
    bot.set_state(call.from_user.id, LowStates.hotel, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=LowStates.hotel)
def hotel_id_chose(call: CallbackQuery) -> None:
    """
    Функция которая принимает все Callback данные за если пользователь находится в состоянии LowStates.hotel

    Присваивает данные Callback (id отеля) в хранилище пользователя.
    Присваетвает пользователю состояние AllStates.get_info.

    Args:
        call (CallbackQuery): id отеля
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['hotel_id'] = call.data
        data['command'] = 'low'
    bot.set_state(call.from_user.id, AllStates.get_info, call.message.chat.id)
    bot.send_message(call.message.chat.id,
                     'Отлично, теперь можем посмотреть информацию по отелю!',
                     reply_markup=keyboard1({'Просмотреть информацию по отелю': 'look'}))
