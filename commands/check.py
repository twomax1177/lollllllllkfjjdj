from re import T
import data
import database

bot = data.bot


def check(channel, message):
    try:
        if bot.get_chat_member(channel, message.chat.id).status == 'left':
            return False
        else:
            return True
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')
