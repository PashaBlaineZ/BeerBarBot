import telebot
import time
import sqlite3
import random

con = sqlite3.connect("bars.db")

cur = con.cursor()

bot = telebot.TeleBot('6594295485:AAEhDrdkD0L5Fvem3qdTPz7jmT9JUR6bd0c')

citysides = ['Центр', 'Северо-Запад', 'Север', 'Северо-Восток', 'Восток', 'Юго-Восток', 'Юг', 'Юго-Запад', 'Без разницы']
bartypes = ['Дешевое','Дорогое', 'Для свидания', 'Для большой компании', 'Выпить в одиночку', 'Живая музыка', 'Высокие оценки', 'Атмосфера', 'Вкусная еда', 'Кальяны и лаунж-зона']
question1 = {'question':'Выбери район, в котором ты хочешь найти бар:', 'options': citysides}
question2 = {'question': 'Выбери тип бара, который ты предпочитаешь:', 'options': bartypes}

user_answers = {}
user_states = {}

for characteristic in bartypes:
    cur.execute("INSERT INTO bar_characteristics (characteristic_name) VALUES (?)", (characteristic,))

con.commit()
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_answers[user_id] = {}
    user_states[user_id] = 'question1'
    bot.send_message(message.chat.id,
                     'Привет, я BarNet. Я создан для того чтобы помочь найти тебе бар по твоему запросу')
    time.sleep(2)
    bot.send_message(message.from_user.id,
                     'Просто выбери из списка пожелания для бара')
    time.sleep(2)
    bot.send_poll(user_id, question=question1['question'], options=question1['options'],
                  allows_multiple_answers=True, is_anonymous=False)

@bot.poll_answer_handler()
def handle_poll(poll):
    user_id = poll.user.id
    question_id = poll.poll_id
    option_ids = poll.option_ids
    user_answers[user_id][question_id] = option_ids

    current_state = user_states.get(user_id)

    if current_state == 'question1':
        user_states[user_id] = 'question2'

        bot.send_poll(user_id, question=question2['question'], options=question2['options'],
                      allows_multiple_answers=True, is_anonymous=False)
    elif current_state == 'question2':
        user_states.pop(user_id)
        bot.send_message(user_id, 'Спасибо за ответы. Сейчас попробую подобрать что-нибудь для вас...')
        time.sleep(2)

        find_a_bar(user_id, user_answers)


def find_a_bar(user_id, user_answers):
    answers = list(user_answers[user_id].values())
    user_sides = [citysides[i] for i in answers[0]]
    print(user_sides)
    print(type(user_sides))
    if 'Без разницы' in user_sides:
        user_sides = citysides
    user_types = [bartypes[i] for i in answers[1]]
    conn = sqlite3.connect("bars.db")
    cursor = conn.cursor()
    user_id = int(user_id)
    results = []
    found = False
    for user_side in user_sides:
        for user_type in user_types:
            cursor.execute("""
                SELECT *
                FROM bars
                WHERE side = ? OR bar_id IN (
                    SELECT bar_id
                    FROM bar_characteristic_relationship
                    WHERE characteristic_id = ?
                )
            """, (user_side, user_type))

            # Получите результаты запроса и добавьте их в список результатов
            results.extend(cursor.fetchall())

    if not results:
        bot.send_message(user_id, 'Не нашёл вариантов по твоему запросу... попробуй ещё раз')
    else:
        final = random.choice(results)
        message = f'Нашёл вариант по твоим запросам:' + '\nБар называется: ' + final[1] + '\nНаходится на: ' + \
                    final[4] + '\nНомер для связи: ' + final[3]
        bot.send_message(user_id, message)
        found = True  # Устанавливаем флаг в True, так как нашли бар

    if not found:
        bot.send_message(user_id, 'Не нашёл вариантов по твоему запросу... попробуй ещё раз')



bot.infinity_polling()
