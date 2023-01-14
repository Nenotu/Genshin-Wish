import random
import telebot
from telebot import types
from os import path
import time

token = '5410798667:AAHLil9PaVdfFc-fh5LduOL5p_t0MGroNYo'
bot = telebot.TeleBot(token)
primogems = 0
epic_guarantor = 0
leg_guarantor = 0
rarities = ['★★★★★', '★★★★', '★★★']
items = {'★★★★★':['Нефритовый коршун', 'Драгоценный омут'], '★★★★':['Амэнома Кагэути', 'Кагоцурубэ Иссин'], '★★★':['Небесный атлас', 'Небесное величие', 'Небесный меч', 'Небесное крыло',]}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Получить примогемы💎')
    btn2 = types.KeyboardButton('История')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Добро пожаловать в рерол банеров ', reply_markup=markup)


def reroll():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'Крутить 1 раз💫'
    btn2 = 'Крутить 10 раз💫'
    btn3 = 'Мои примогемы🔎'
    btn4 = 'Получить примогемы💎'
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def gacha(roll_count):
    global leg_guarantor, epic_guarantor
    drop = {'★★★★★':[], '★★★★':[], '★★★':[]}
    for roll in range(roll_count):
        drop_star = random.choices(rarities, weights = [0.6, 5.1, 94.3])[0] #k= несколько выбранных
        if leg_guarantor == 90 and drop_star != '★★★★★':
            drop_star = '★★★★★'
            leg_guarantor = 0
        elif epic_guarantor == 10 and drop_star != '★★★★':
            drop_star = '★★★★'
            epic_guarantor = 0
        elif drop_star == '★★★':
            leg_guarantor += 1
            epic_guarantor += 1
        elif drop_star == '★★★★':
            leg_guarantor += 1
            epic_guarantor = 0
        elif drop_star == '★★★★★':
            leg_guarantor = 0
            epic_guarantor += 1
        drop[drop_star].append(random.choice(items[drop_star]))
    return drop
#join список в строку
#split из строки список
def form_weapon_in_mes(drop):
    mes = ''
    if drop['★★★★★']:#if проверяет на пустоту
        drop['★★★★★'] = ['★★★★★' + i for i in drop['★★★★★']]
        mes +='\n'.join(drop['★★★★★']) + '\n'
    if drop['★★★★']:
        drop['★★★★'] = ['★★★★' + i for i in drop['★★★★']]
        mes +='\n'.join(drop['★★★★']) + '\n'
    if drop['★★★']:
        drop['★★★'] = ['★★★' + i for i in drop['★★★']]
        mes +='\n'.join(drop['★★★']) + '\n'
    return mes

@bot.message_handler(content_types=['text'])
def game_body(message):
    global primogems, leg_guarantor, epic_guarantor, rarities
    if message.text == 'Получить примогемы💎':
        primogems += 1600
        bot.send_message(message.chat.id, text='Теперь ты можешь покрутить', reply_markup=reroll())

    if message.text == 'Историю':
        primogems += 1600
        bot.send_message(message.chat.id, text='Теперь ты можешь покрутить', reply_markup=reroll())

    if message.text == 'Мои примогемы🔎':
        bot.send_message(message.chat.id, text=f'Примогемы: {primogems}')

    if message.text == 'Крутить 1 раз💫':
        if primogems >= 160:
            primogems -= 160
            drop = gacha(1)
            if drop['★★★★★']:
                animation = 'https://tenor.com/ru/view/genshin-impact-wish-genshin-legendary-orange-gif-26472706'
                photo = open(rf"img\{drop['★★★★★'][0]}.jpg", 'rb')
            elif drop['★★★★']:
                animation = 'https://tenor.com/ru/view/genshin-wish-genshin-impact-rare-purple-gif-26472708'
                photo = open(rf"img\{drop['★★★★'][0]}.jpg", 'rb')
            elif drop['★★★']:
                animation = 'https://tenor.com/ru/view/genshin-impact-wish-common-gif-26472698'
                photo = open(rf"img\{drop['★★★'][0]}.jpg", 'rb')
            msg = bot.send_animation(message.chat.id, animation=animation)
            time.sleep(5.55)
            bot.delete_message(message.chat.id, msg.message_id)
            mes = form_weapon_in_mes(drop)
            bot.send_photo(message.chat.id, photo, caption=f'{message.from_user.first_name}, тебе выпал:\n<b>{mes}</b>', parse_mode='HTML')
            photo.close()
        else:
            bot.send_message(message.chat.id, text='Извините у вас не хватает примогемов', reply_markup=reroll())

    if message.text == 'Крутить 10 раз💫':
        if primogems >= 1600:
            primogems -= 1600
            drop = gacha(10)
            if drop['★★★★★']:
                animation = 'https://tenor.com/ru/view/genshin-impact-wish-genshin-legendary-orange-gif-26472706'
                photo = open(rf"img\{drop['★★★★★'][0]}.jpg", 'rb')
            elif drop['★★★★']:
                animation = 'https://tenor.com/ru/view/genshin-wish-genshin-impact-rare-purple-gif-26472708'
                photo = open(rf"img\{drop['★★★★'][0]}.jpg", 'rb')
            elif drop['★★★']:
                animation = 'https://tenor.com/ru/view/genshin-impact-wish-common-gif-26472698'
                photo = open(rf"img\{drop['★★★'][0]}.jpg", 'rb')
            msg = bot.send_animation(message.chat.id, animation=animation)
            time.sleep(5.55)
            bot.delete_message(message.chat.id, msg.message_id)
            mes = form_weapon_in_mes(drop)
            bot.send_photo(message.chat.id, photo, caption=f'{message.from_user.first_name}, тебе выпали:\n<b>{mes}</b>', parse_mode='HTML')
            photo.close()
        else:
            bot.send_message(message.chat.id, text='Извините у вас не хватает примогемов', reply_markup=reroll())


bot.polling(non_stop=True)
