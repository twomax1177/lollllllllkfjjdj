import data
from commands import start, buttons_handler

bot = data.bot
import database
db = database.db
bot_coll = db['bot']


if not bot_coll.find_one({"bot_id": bot.get_me().id}):
    bot_coll.insert_one(database.bot_coll(bot.get_me().id))



bot.delete_webhook()
print(bot.get_me().username)
bot.polling(none_stop=True)

