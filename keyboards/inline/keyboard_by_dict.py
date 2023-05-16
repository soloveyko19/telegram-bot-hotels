from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def keyboard1(info: dict = None, back: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    if info:
        for element, value in info.items():
            keyboard.add(InlineKeyboardButton(text=element, callback_data=value))
    if back:
        keyboard.add(InlineKeyboardButton(text='↩️ Вернуться в главное меню', callback_data='cancel'))
    return keyboard
