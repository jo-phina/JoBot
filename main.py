from config import TELEGRAM_API, LOCAL_SERVER_API
import telebot
import requests
import json

# required: python file config.py with APIs to Telegram bot and to local server, i.e., TELEGRAM_API = " " and LOCAL_SERVER_API = " "
# or define here:
# TELEGRAM_API = ""
# LOCAL_SERVER_API = ""

# instantiating bot
bot = telebot.TeleBot(token=TELEGRAM_API)  # refers to my bot in telegram

# @bot.message_handler() handles messages. whatever function comes afterwards will be used

@bot.message_handler(commands=['start'])    # answer \start request
def welcome(msg):
    welcome_text = f"Hello {msg.from_user.first_name}, welcome to JoBot! I am an confused AI assistant - maybe I can help you, but probably not..."
    bot.send_message(msg.chat.id, welcome_text)


@bot.message_handler(commands=['help']) # answer \help request
def help(msg):
    help_text = f"I'm sorry, {msg.from_user.first_name}, I worry I won't be able to help since I'm still a tiny llama. But you can try if you want - just don't rely on me!"
    bot.send_message(msg.chat.id, help_text)

@bot.message_handler(regexp="help") # reaction if word "help" is in a message
def handle_help(msg):
    help_text = f"I'm sorry, {msg.from_user.first_name}, I can't help you since I'm still a very tiny llama. Maybe you can ask someone else?"
    picture = open("./HW/HW9/tinyllama_confused.jpg",'rb')
    bot.send_photo(msg.chat.id, photo=picture, caption=help_text)
    picture.close()


@bot.message_handler(regexp="llama")    # reaction if word "llama" is in a message'
def handle_llame(msg):
    bot.reply_to(msg, "Do you mean me?? I'm a tiny llama! ❤️🦙")


# using tinyLlama to answer messages to bot
@bot.message_handler(func=lambda message:True)
def reply_to_message(msg):
    # bot.reply_to(message, text="Your message has been lost in the depths of the internet.")
    incoming_text = msg.text

    # dict with api data for the API request
    api_data = {
        "messages": [{"role": "user", "content": incoming_text}],
        "temperature": 0.7,
        "max_tokens": 500,
        "stream": False
    }

    # make request to API of my local server running on LM Studio
    resp = requests.post(url=LOCAL_SERVER_API, json=api_data, headers={"Content-Type": "application/json"})

    if resp.status_code == 200:
        api_resp = json.loads(resp.text)    # get response text from API

        # TinyLlama assistant's answer from the API response
        TinyLlama_resp = api_resp["choices"][0]["message"]["content"]

        bot.reply_to(msg, TinyLlama_resp)
    
    else:   # if the API request does not work somehow
        bot.reply_to(msg, "Something went wrong with the API request and your message has been lost in the depths of the internet.")



if __name__ == "__main__":
    bot.polling(none_stop=True)