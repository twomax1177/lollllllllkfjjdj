import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from commands import start, statics, texts
import data
import database

bot = data.bot
db = database.db

@bot.callback_query_handler(func=lambda call: True)
def handle_call(call):
    if 'continue' in call.data:
        start.continue_button(call)
        return


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == '✅ Join Airdrop':
        start.join_airdrop(message)
        return
    elif message.text == '✅ Submit Details':
        start.submit_details(message)
        return
    elif message.text == '✅ Join':
        start.join_button(message)
        return
    elif message.text == 'Statistics':
        statics.statics(message)
        return
    elif message.text == '🚫 Cancel':
        markup = ReplyKeyboardRemove()
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.send_message(message.chat.id, texts.cancel_text, reply_markup=markup)
        return
