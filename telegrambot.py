import os
from requests.api import request
import telebot
from chatbot import chatbot_response
from movie import recommend_movie

API_KEY = "2017656850:AAFDSlOSw0ayk8VwVCBOwTjq-UGurGMHsOo"

bot = telebot.TeleBot(API_KEY)



def check_bot(message):
    request = list(message.text)
    for i in request:
        if i == "/":
            return True
        else:
            return False


@bot.message_handler(func=check_bot)
def talk(message):
    request = message.text.split("/")[1]
    bot.send_message(message.chat.id,chatbot_response(request))


# def check(message):
#     request = message.text.split("/")
#     if len(request) < 2:
#         return False
#     else:
#         return True

@bot.message_handler()

def send(message):
    request = message.text
    print(request)
    bot.send_message(message.chat.id,"Please wait, recommeding movies.....")
    recommend_movie(request)    
    with open("recommendations.txt", "r") as f:
        contents = f.read()

    bot.send_message(message.chat.id,contents.replace("Â",""))

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)

bot.polling()


# bot.polling()

