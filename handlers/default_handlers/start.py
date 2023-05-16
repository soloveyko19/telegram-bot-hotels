from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline.keyboard_by_dict import keyboard1
from states.states import LowStates, HighStates, CustomStates


@bot.message_handler(commands=["start"], state=None)
def bot_start(message: Message) -> None:
    bot.send_message(message.chat.id,
                     f'Приветсвую, {message.from_user.first_name}!\n'
                     f'Я бот созданный для помощи в поисках отелей',
                     reply_markup=keyboard1({
                        'Начать поиск отелей': 'start_survey'
                     }))


@bot.callback_query_handler(func=lambda call: call.data in ('start_survey', 'low', 'high', 'custom'), state=None)
def type_of_sort(call: CallbackQuery) -> None:
    if call.data == 'start_survey':
        bot.send_message(call.message.chat.id,
                         'Хорошо, теперь выберите как будем искать отели:',
                         reply_markup=keyboard1({
                             'Самые дешевые номера': 'low',
                             'Самые дорогие номера': 'high',
                             'Ваш диапазон цен': 'custom'
                         }))
    elif call.data == 'low':
        bot.send_message(call.message.chat.id,
                         'Отлично, будем искать самые дешевые отели!\n'
                         'Теперь введи с клавиатуры название города в котором будем искать отели.\n'
                         )
        bot.set_state(call.from_user.id, LowStates.city, call.message.chat.id)
    elif call.data == 'high':
        bot.send_message(call.message.chat.id,
                         'Отлично, будем искать самые дорогие номера!\n'
                         'Теперь введи с клавиатуры название города в котором будем искать отели.\n'
                         )
        bot.set_state(call.from_user.id, HighStates.city, call.message.chat.id)
    elif call.data == 'custom':
        bot.send_message(call.message.chat.id,
                         'Отлично, будем искать отели в вашем ценовом диапазоне!\n'
                         'Теперь введи с клавиатуры название города в котором будем искать отели.\n')
        bot.set_state(call.from_user.id, CustomStates.city, call.message.chat.id)
