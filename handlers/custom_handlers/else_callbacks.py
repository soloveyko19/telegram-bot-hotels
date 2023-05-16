""" Модуль отвечающий за сброс состояния пользователя и просмотр информации по отелю """


from telebot.types import CallbackQuery, InputMediaPhoto
from keyboards.inline.keyboard_by_dict import keyboard1
from loader import bot
from states.states import AllStates
from utils.misc.api_requests import get_hotel_info
from database.db_functions import add_hotel


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def cancel_states(call: CallbackQuery) -> None:
    """ Функция сбрасывающая состояние пользователя """
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Вы вернулись в главное меню!\n'
                                           'Подсказки тут /help')


@bot.callback_query_handler(func=lambda call: True, state=AllStates.get_info)
def view(call: CallbackQuery) -> None:
    """ Функция вывода всех всей информации по отелю """
    if call.data == 'look_photos':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.send_media_group(call.message.chat.id,
                                 [InputMediaPhoto(img) for img in data['hotel_info']['img_urls']])
            bot.send_message(call.message.chat.id,
                             f'Фотографии отеля {data["hotel_info"]["name"]}',
                             reply_markup=keyboard1({
                                 'Назад': 'back',
                             }))
    elif call.data == 'send_geolocation':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.send_location(call.message.chat.id,
                              data['hotel_info']['coordinates']['x'],
                              data['hotel_info']['coordinates']['y'],
                              reply_markup=keyboard1({
                                  'Назад': 'back',
                              }))
    else:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            info = data.get('hotel_info')
            if not info:
                info = get_hotel_info(data['hotel_id'])
                data['hotel_info'] = info
                add_hotel(info['name'], call.from_user.id, data['command'])
        rating = info.get('rating')
        bot.send_message(call.message.chat.id,
                         f'Название: {info["name"]}\n'
                         f'Рейтинг: {rating + "⭐" if rating else "Без рейтинга"}\n'
                         f'Адресс: {info["address"]}\n'
                         f'Об отеле: {info["tagline"]}',
                         reply_markup=keyboard1({
                             'Посмотреть фотографии отеля': 'look_photos',
                             'Посмотреть на карте': 'send_geolocation',
                         }, back=True))
