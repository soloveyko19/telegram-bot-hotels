from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Я не понял что вы имели ввиду(\n/help"
    )
