import telebot
from telebot import types

bot = telebot.TeleBot('6673082886:AAFC55vhG-xxfAy6nxWtc5_qDmQpumJHDn8')

user_answers = {}




#['Живописный вид', "Дешевый", "Для свидания", "На вынос", "Пляж", "Своя пивоварня", "Сезонные предложения", "Шведский стол"]


# начало с кнопкой "старт"
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_answers[user_id] = {}
    bot.send_message(message.from_user.id,
                     'Привет, я BeerBarBot. Я создан для того чтобы помочь найти тебе бар по твоему запросу')
    bot.send_message(message.from_user.id,
                     'Просто выбери из списка пожелания для бара')
    question1 = ['Центр', 'Северо-Запад', 'Север', 'Северо-Восток', 'Восток', 'Юго-Восток', 'Юг', 'Юго-Запад', 'Без разницы']
    p1 = bot.send_poll(user_id, 'Просто выбери из списка пожелания для бара', question1, allows_multiple_answers=True)
    payload1 = p1.poll.id: {
        'questions':question1,
        'message':poll_id
    }




bot.polling(none_stop=True, interval=0)
