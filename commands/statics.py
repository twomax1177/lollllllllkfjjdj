

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
import data as datab
import database
from commands import check, texts
check = check.check

bot = datab.bot
db = database.db

def statics(message):
    try:
        markup = ReplyKeyboardMarkup(True)
        markup.row('Statistics')
        data = db['users'].find_one({'user_id': message.chat.id})
        bot.send_message(message.chat.id, texts.static_text.format(name=message.chat.first_name, wallet=data['wallet'], ref_count=data['invite_count'], bot_name=bot.get_me().username, user_id=message.chat.id, twitter=data['twitter'], reply_markup=markup, disable_web_page_preview = True))
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')

