from config import *

from telegram.ext import Updater, MessageHandler, Filters
import requests
import re

from dialogflow import *

def main():
    updater = Updater(TELEGRAM_BOT_KEY)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all,bop))
    print("start bot")
    updater.start_polling()
    updater.idle()

def bop(bot, update):
    print("hi")
    userid = update.message.chat_id
    print(userid)
    print(update.message)
    msgs = handle_user_message(update.message.text, userid)
    print(msgs)
    for msg in msgs:
        if isinstance(msg, str):
            bot.send_message(chat_id=userid, text=msg)
        else:
            #it's an image object
            bot.send_photo(chat_id=userid, photo=open(msg["path"], 'rb'))
    
if __name__ == '__main__':
    main()