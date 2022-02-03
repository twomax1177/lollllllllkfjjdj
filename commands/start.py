

import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
import data
import database
import re
from commands import check, texts, statics
check = check.check

bot = data.bot
db = database.db



# functions



# captcha function

def captcha(message):
    try:
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('continue', callback_data=f'continue {a+b}'))
        bot.send_message(message.chat.id, texts.captcha_message.format(a=a, b=b), reply_markup=markup, disable_web_page_preview = True)
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')

def continue_button(call):
    try:
        if call.data == 'continue':
            return
        ans = call.data.split(' ')[1]
        '*😒Wrong answer!* Please try again.'
        send = bot.send_message(call.message.chat.id, '_Great, please enter the code._')
        bot.register_next_step_handler(send, get_ans, ans=ans)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Debug: {e}')

def get_ans(message, ans):
    try:
        if message.text != ans:
            bot.send_message(message.chat.id, '*😒Wrong answer!* Please try again.')
            return
        markup = ReplyKeyboardMarkup(True)
        markup.add('✅ Join Airdrop', row_width=2)
        db['users'].find_one_and_update({"user_id": message.chat.id}, {'$set': {
            'captcha': True
        }})
        bot.send_message(message.chat.id, texts.start_message.format(name=message.from_user.first_name, join_reward=data.join_reward, end_date=data.end_date, top_10_reward=data.top_10_reward), reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')




# Join Airdrop function

def join_airdrop(message):
    try:
        markup = ReplyKeyboardMarkup(True)
        markup.add('✅ Submit Details', row_width=2)
        bot.send_message(message.chat.id, texts.join_airdrop_text, reply_markup=markup, disable_web_page_preview= True)
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')


# Submit Details Function


def submit_details(message):
    try:
        markup = ReplyKeyboardMarkup(True)
        markup.row('✅ Join')
        bot.send_message(message.chat.id, texts.submit_details_text.format(channel=data.channel, group= data.group, ad_channel=data.ad_channel), reply_markup=markup, disable_web_page_preview = True)
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')


# join button function

def join_button(message):
    try:
        markup = ReplyKeyboardMarkup(True)
        markup.row('✅ Join')

        markup2 = ReplyKeyboardMarkup(True)
        markup2.row('🚫 Cancel')

        # if not check(channel=f'@{data.channel}', message=message):
        #     bot.send_message(message.chat.id, texts.submit_details_text.format(channel=data.channel, group=data.group,
        #                                                                        ad_channel=data.ad_channel),
        #                      reply_markup=markup, disable_web_page_preview = True)
        #     return
        # if not check(channel=f'@{data.group}', message=message):
        #     bot.send_message(message.chat.id, texts.submit_details_text.format(channel=data.channel, group=data.group,
        #                                                                        ad_channel=data.ad_channel),
        #                      reply_markup=markup, disable_web_page_preview = True)
        #     return
        # if not check(channel=f'@{data.ad_channel}', message=message):
        #     bot.send_message(message.chat.id, texts.submit_details_text.format(channel=data.channel, group=data.group,
        #                                                                        ad_channel=data.ad_channel),
        #                      reply_markup=markup, disable_web_page_preview = True)
        #     return
        send = bot.send_message(message.chat.id, texts.twitter_text, reply_markup=markup2, disable_web_page_preview = True)
        bot.register_next_step_handler(send, get_twitter)
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')

def get_twitter(message):
    try:
        markup2 = ReplyKeyboardMarkup(True)
        markup2.row('🚫 Cancel')
        if message.text == '🚫 Cancel':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.send_message(message.chat.id, texts.cancel_text)
            return

        elif 'twitter.com' in message.text:
            db['users'].find_one_and_update({"user_id": message.chat.id}, {'$set': {
                'twitter': message.text
            }})
            send = bot.send_message(message.chat.id, texts.wallet_address_text, reply_markup=markup2, disable_web_page_preview=True)
            bot.register_next_step_handler(send, get_email)
            return

        elif 'Twitter.com' in message.text:
            db['users'].find_one_and_update({"user_id": message.chat.id}, {'$set': {
                'twitter': message.text
            }})
            send = bot.send_message(message.chat.id, texts.wallet_address_text, reply_markup=markup2, disable_web_page_preview=True)
            bot.register_next_step_handler(send, get_email)
            return

        else:
            send = bot.send_message(message.chat.id, '*Invalid twitter provile link!* _Please provide a valid twitter profile link._', reply_markup=markup2)
            bot.register_next_step_handler(send, get_twitter)
            return


    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')


def get_email(message):
    try:

        markup = ReplyKeyboardMarkup(True)
        markup.row('🚫 Cancel')

        markup2 = ReplyKeyboardMarkup(True)
        markup2.row('Statistics')
        if message.text == '🚫 Cancel':
            bot.clear_step_handler_by_chat_id(message.chat.id)
            bot.send_message(message.chat.id, texts.cancel_text)
            return
        elif len(message.text) == 42:
            db['users'].find_one_and_update({"user_id": message.chat.id}, {'$set': {
                'wallet': message.text, 'tasks': True
            }})
            if db['users'].find_one({'user_id':message.chat.id})['invite_by'] and not db['users'].find_one({'user_id':message.chat.id})['invited']:
                invitee = db['users'].find_one({'user_id':message.chat.id})['invite_by']
                bot_data = db['bot'].find_one({"bot_id": bot.get_me().id})
                bot.send_message(invitee, f'*➕ You earned {format(bot_data["refer_bonus"], ".7f")} {data.bot_currency} from a refferal*')
                db['users'].find_one_and_update({'user_id': message.chat.id}, {'$set': {'invited': True}})
                db['users'].find_one_and_update({'user_id': invitee}, {'$inc': {'balance': bot_data['refer_bonus'], 'invite_count': 1}})


            bot.send_message(message.chat.id, texts.task_done_text.format(name=message.from_user.first_name, bot_name=bot.get_me().username, user_id=message.chat.id), reply_markup=markup2, disable_web_page_preview = True)
            return
        else:
            send = bot.send_message(message.chat.id, texts.wallet_address_text, reply_markup=markup, disable_web_page_preview=True)
            bot.register_next_step_handler(send, get_email)
            return
    except Exception as e:
        bot.send_message(message.chat.id, f'Debug: {e}')









@bot.message_handler(commands=['start'])
def start(message):
        if message.text == '/start':
            try:
                if not db['users'].find_one({"user_id": message.chat.id}):
                    coll = database.users_coll(message.chat.id)
                    db['users'].insert_one(coll)
                    db['bot'].find_one_and_update({'bot_id': bot.get_me().id}, {'$inc': {'total_users': 1}})
                if not db['users'].find_one({"user_id": message.chat.id})['captcha']:
                    captcha(message)
                    return
                if not db['users'].find_one({"user_id": message.chat.id})['tasks']:
                    markup = ReplyKeyboardMarkup(True)
                    markup.add('✅ Join Airdrop')
                    bot.send_message(message.chat.id, texts.start_message.format(name=message.from_user.first_name, join_reward=data.join_reward, end_date=data.end_date, top_10_reward=data.top_10_reward), reply_markup=markup)
                    return
                else:
                    statics.statics(message)
                    return
            except Exception as e:
                bot.send_message(message.chat.id,f'Debug: {e}')
        elif message.text == '/start resubmit':
            try:
                markup = ReplyKeyboardMarkup(True)
                markup.add('✅ Join Airdrop')
                bot.send_message(message.chat.id,
                                 texts.start_message.format(name=message.from_user.first_name,
                                                            join_reward=data.join_reward,
                                                            end_date=data.end_date, top_10_reward=data.top_10_reward),
                                 reply_markup=markup)
                return
            except Exception as e:
                bot.send_message(message.chat.id, f'Debug: {e}')
        else:
            try:
                if not db['users'].find_one({"user_id": message.chat.id}):
                    coll = database.users_coll(message.chat.id, int(message.text.split(' ')[1]))
                    db['users'].insert_one(coll)
                    db['bot'].find_one_and_update({'bot_id': bot.get_me().id}, {'$inc': {'total_users': 1}})
                if not db['users'].find_one({"user_id": message.chat.id})['captcha']:
                    captcha(message)
                    return
                if not db['users'].find_one({"user_id": message.chat.id})['tasks']:
                    markup = ReplyKeyboardMarkup(True)
                    markup.add('✅ Join Airdrop')

                    bot.send_message(message.chat.id, texts.start_message.format(name=message.from_user.first_name,
                                                                                 join_reward=data.join_reward,
                                                                                 end_date=data.end_date,
                                                                                 top_10_reward=data.top_10_reward), reply_markup= markup)
                    return
                else:
                    statics.statics(message)
                    return


            except Exception as e:
                bot.send_message(message.chat.id,f'Debug: {e}')


