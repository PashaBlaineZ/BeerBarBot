import telebot
from telebot import types

bot = telebot.TeleBot('6673082886:AAFC55vhG-xxfAy6nxWtc5_qDmQpumJHDn8')


user_answers = {}

questions = {
    1: {'question': 'Район', 'options': ['Адмиралтейский', 'Василеостровский', 'Выборгский', 'Калининский', 'Кировский', 'Колпинский', 'Красногвардейский', 'Красносельский', 'Кронштадтский', 'Курортный',
                                         'Московский', 'Невский', 'Петроградский', 'Петродворцовый', 'Приморский', 'Пушкинский', 'Фрунзенский', 'Центральный', 'Ленинградская область']},
    2: {'question':}
}
# начало с кнопкой "старт"
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(message.from_user.id, 'Привет, я BeerBarBot. Я создан для того чтобы помочь найти тебе бар по твоему запросу')
    bot.send_message(message.from_user.id,
                     'Просто выбери из списка пожелания для бара')
    bot.send_poll()
@bot.message_handler(func=lambda message: message.text.lower() == 'ваш текст')
def find_near(message):
    bot.send_message(message.from_user.id,)

def poll(user_id):



bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
