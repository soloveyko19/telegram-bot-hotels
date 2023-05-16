""" Модуль комманды /custom """


from telebot.types import Message, CallbackQuery
from keyboards.inline.keyboard_by_dict import keyboard1
from loader import bot
from states.states import CustomStates, AllStates
from utils.misc.api_requests import get_city, get_hotels


@bot.message_handler(commands=['custom'], state=None)
def custom_start(message: Message) -> None:
    """
    Функция начала опроса по комманде /custom

    Присваивает пользователю начальное состояние для поиска города

    Args:
        message (Message): сообщение пользователя
    """
    bot.set_state(message.from_user.id, CustomStates.city, message.chat.id)
    bot.send_message(message.chat.id,
                     'Отлично, будем искать отели в вашем ценовом диапазоне!\n'
                     'Теперь введи с клавиатуры название города в котором будем искать отели.\n')


@bot.message_handler(state=CustomStates.city)
def get_city_info(message: Message) -> None:
    """
    Функцияя вывода найденных городов из функции get_city.

    Если найденных городов больше одного то выводится inline клавиатура надписью на которой является имя города,
    а параметром callback является id этого города.
    Если найденный город только один, то сразу присваивается в хранилище id этого города и следущее состояние
    пользователю (Customstates.price_from).
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
        bot.send_message(message.chat.id,
                         'Хорошо, теперь введи минимальную цену за номер в отеле в долларах')
        bot.set_state(message.from_user.id, CustomStates.price_from)
    else:
        bot.send_message(message.chat.id,
                         f'Город {message.text.capitalize()} не найден.\n'
                         f'Убедись что ввел город правильно и попробуй еще раз',
                         reply_markup=keyboard1(back=True))


@bot.message_handler(state=CustomStates.price_from)
def price_from_chose(message: Message) -> None:
    """
    Функция получения от пользователя минимальной цены для поиска отелей

    Обрабатывает сообщение и проверяет чтобы число было более 0 но не более 35 000.
    В случае полного соотвествия требованиям присваивается следующее состояние (CustomState.price_to)
    В случае несоответсвия выводит соответствующее сообщение

    Args:
        message (Message): сообщение пользователя (минимальная цена за отель)
    """
    try:
        price = int(message.text)
        if price < 0:
            bot.send_message(message.chat.id,
                             'Слишком маленькое числовое значение, минимальная цена 0$')
        elif price > 35000:
            bot.send_message(message.chat.id,
                             'Слишком большое числовое значение, максимальная цена 35 000$.')
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['price_from'] = message.text
            bot.send_message(message.chat.id,
                             'Хорошо, теперь введите максимальную цену отеля в долларах')
            bot.set_state(message.chat.id, CustomStates.price_to, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id,
                         'Пожалуйста введите корректную минимальную цену за номер в отеле')


@bot.message_handler(state=CustomStates.price_to)
def price_to_chose(message: Message) -> None:
    """
    Функция получения от пользователя максимальной цены для поиска отелей

    Обрабатывает сообщение и проверяет чтобы число было более минимальной цены но не более 100 000.
    В случае полного соотвествия требованиям присваивается следующее состояние (CustomState.hotel)
    В случае несоответсвия выводит соответствующее сообщение.

    Args:
        message (Message): сообщение пользователя (максимальнаяя цена за отель)
    """
    try:
        price = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if price < int(data['price_from']):
                bot.send_message(message.chat.id,
                                 'Максимальная цена не может быть больше минимальной цены!')
            elif price > 100000:
                bot.send_message(message.chat.id,
                                 'Максимальное значение 100 000!')
            else:
                data['price_to'] = message.text
                bot.send_message(message.from_user.id,
                                 f'Хорошо, давай дальше.\n'
                                 'Введи количество отелей для вывода\n'
                                 '(от 1 до 10 включительно)')
                bot.set_state(message.from_user.id, CustomStates.hotel)
    except ValueError:
        bot.send_message(message.chat.id,
                         'Пожалуйста введите корректную максимальную цену за номер в отеле')


@bot.message_handler(state=CustomStates.hotel)
def chose_hotels_amount(message: Message) -> None:
    """
    Функция поиска отеля по данным введенные пользователем ранее

    Проверяет что число отелей которое ввел пользователь больше 0 но не более 10
    Если все условия проходят то пользователю выдается клавиатура с названием отелей, значением callback которых
    является id этого отеля

    Args:
        message (Message): сообщение пользователя (кол-во отелей для вывода)
    """
    try:
        amount = int(message.text)
        if amount > 10:
            bot.send_message(message.chat.id,
                             'Выбрано слишком много отелей, пожалуйста введи число от 1 до 10')
        elif amount < 1:
            bot.send_message(message.chat.id,
                             'Выбрано слишком мало отелей, пожалуйста введи число от 1 до 10')
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotels_amt'] = amount
                bot.send_message(message.chat.id, 'Поиск отелей...')
                result = get_hotels(data['city_id'], amount, 'RECOMMENDED',
                                    price=(data['price_from'], data['price_to']))
                if result:
                    bot.send_message(message.chat.id, 'Выберите отель', reply_markup=keyboard1(result, back=True))
                else:
                    bot.send_message(message.chat.id,
                                     'К сожалению отелей в вашем ценовом диапазоне не было найдено.\n'
                                     'Вы вернулись в главное меню /help')
                    bot.delete_state(message.from_user.id, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста введите целое число от 1 до 10')


@bot.callback_query_handler(func=lambda call: True, state=CustomStates.city)
def city_id_chose(call: CallbackQuery) -> None:
    """
    Функция которая принимает все Callback если пользовательь находится в состоянии CustomStates.city

    Присваивает данные Callback (id города) в хранилище пользователя

    Args:
        call (CallbackQuery): id города
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['city_id'] = call.data
    bot.send_message(call.message.chat.id,
                     'Хорошо, теперь введи минимальную цену за номер в отеле в долларах')
    bot.set_state(call.from_user.id, CustomStates.price_from)


@bot.callback_query_handler(func=lambda call: True, state=CustomStates.hotel)
def hotel_id_chose(call: CallbackQuery) -> None:
    """
    Функция которая принимает все Callback данные за если пользователь находится в состоянии CustomStates.hotel

    Присваивает данные Callback (id отеля) в хранилище пользователя.
    Присваетвает пользователю состояние AllStates.get_info.

    Args:
        call (CallbackQuery): id отеля
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['hotel_id'] = call.data
        data['command'] = 'custom'
    bot.set_state(call.from_user.id, AllStates.get_info, call.message.chat.id)
    bot.send_message(call.message.chat.id,
                     'Отлично, теперь можем посмотреть информацию по отелю!',
                     reply_markup=keyboard1({'Просмотреть информацию по отелю': 'look'}))

