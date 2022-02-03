
import data
bot = data.bot
client = data.client
db = client[f'{bot.get_me().username}-test']



def users_coll(user_id, refer_id=None):
    users = {
        "user_id": user_id,
        "captcha": False,
        "tasks": False,
        "twitter": None,
        "wallet": 'not set',
        "balance": 0.0000,
        "withdrawn": 0.0000,
        "bonus_time": None,
        "invited": False,
        "invite_by": refer_id,
        "invite_count": 0

    }
    return users

def bot_coll(bot_id):
    bot = {
        "bot_id": bot_id,
        "currency": data.bot_currency,
        "total_withdrawn": 0.0000,
        "total_users": 0,
        "refer_bonus": 0.0000015,
        "min_withdraw": 0.000003,
        "payment_channel": None,
        "coinbase_api_key": None,
        "coinbase_secret_key":None
    }
    return bot
