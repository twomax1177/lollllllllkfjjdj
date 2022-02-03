import telebot
import pymongo


#mongo uri link
uri = "mongodb+srv://AirdropBot:Venom1@cluster1.bosd1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)


#bot_data

admin = 822062554 #owner
bot_currency = 'SOL' # bot currency
join_reward = 10
end_date = '12 Feb 2022'
top_10_reward = 10


pay_channel = '@ShibInuBot_pay'
channel = 'Airdrops_detectors' #without @
group = 'Airdrops_detecto' #without @
ad_channel = 'AirdropAchiever' #without @
twitter = 'adtteam1' #without @
twitter_post = 'lolo'




token = 'Your bot token'
bot = telebot.TeleBot(token, parse_mode='markdown')

