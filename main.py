import telebot
import requests
import json

bot = telebot.TeleBot('token')
API = 'API key'


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hello, {message.from_user.first_name}! Write the name of the city'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Temperature now: {temp}')

        image = 'sun.png' if temp > 25 else 'cold.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file.read())
    else:
        bot.reply_to(message, "City is incorrect!")


bot.polling(none_stop=True)