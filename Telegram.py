import telebot, os
import api_token
import time
import requests
import random
import json

if not os.path.exists('Images'):
    os.mkdir('Images')
if not os.path.exists('Results'):
    os.mkdir('Results')

from MemeGen import MemeGenerator
from Settings import settings as Settings

bot = telebot.TeleBot(api_token.token)
directory = os.getcwd()

def sendImage(chat_id, file_path, message_id):
    url = f"https://api.telegram.org/bot{api_token.token}/sendPhoto";
    files = {'photo': open(file_path, 'rb')}
    data = {'chat_id': chat_id}
    if message_id != -1:
        data.update({'reply_to_message_id': message_id})
    r = requests.post(url, files=files, data=data)

def randomHex():
    return '#'+hex(random.randint(0, 16777215))[2:].upper()

class Counter:
    def __init__(self):
        self.value = 0
    def inc(self):
        self.value += 1
        print('\rКоличество рофлянок: '+str(self.value), end='')
counter = Counter()

@bot.message_handler(commands=['help'])
def help(message):
    sendImage(message.chat.id, f'Guide\\sending_with_text.png', -1)
    bot.send_message(message.chat.id, """Отправьте фотографию либо фотографию + текст
Разделение строк по символу \"\\\'""")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Повезло повезло, бот работает!\nПомощь /help')

@bot.message_handler(commands=['settings'])
def settings(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton('Расположение', callback_data=json.dumps({"changing": "place", "id": str(message.id+1)}))
    button_2 = telebot.types.InlineKeyboardButton('Шрифт', callback_data=json.dumps({"changing": "font", "id": str(message.id+1)}))
    keyboard.add(button_1, button_2)
    bot.send_message(chat_id=message.chat.id, text='Настройки:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda messsage: True)
def change_settings(call):
    info = json.loads(call.data)

    if info['changing'] == 'place':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_1 = telebot.types.InlineKeyboardButton('На картинке',
                                                      callback_data=json.dumps({'changing':'place_now', 'type': 'on_image', 'id': call.message.id}))
        button_2 = telebot.types.InlineKeyboardButton('Под картинкой',
                                                      callback_data=json.dumps({'changing':'place_now', 'type': 'under_image', 'id': call.message.id}))
        keyboard.add(button_1, button_2)
        bot.edit_message_text(text='Выберите расположение', chat_id=call.message.chat.id, message_id=int(info['id']),
                              reply_markup=keyboard)

    if info['changing'] == 'font':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_1 = telebot.types.InlineKeyboardButton('Impact',
                                                      callback_data=json.dumps({'changing':'font_now', 'type': 'impact', 'id': call.message.id}))
        button_2 = telebot.types.InlineKeyboardButton('Lobster',
                                                      callback_data=json.dumps({'changing':'font_now', 'type': 'lobster', 'id': call.message.id}))
        keyboard.add(button_1, button_2)
        bot.edit_message_text(text='Выберите шрифт', chat_id=call.message.chat.id, message_id=int(info['id']), reply_markup=keyboard)

    if info['changing'] == 'place_now':
        Settings.place.add(call.message.chat.id, info['type'])

        keyboard = telebot.types.InlineKeyboardMarkup()
        button_1 = telebot.types.InlineKeyboardButton('Вернутся к настройкам', callback_data=json.dumps(
            {"changing": "go_to_menu", "id": str(call.message.id)}))
        keyboard.add(button_1)

        bot.edit_message_text(text='Настройки сохранены.', chat_id=call.message.chat.id, message_id=int(info['id']), reply_markup=keyboard)

    if info['changing'] == 'font_now':
        Settings.font.add(call.message.chat.id, info['type'])

        keyboard = telebot.types.InlineKeyboardMarkup()
        button_1 = telebot.types.InlineKeyboardButton('Вернуться к настройкам', callback_data=json.dumps(
            {"changing": "go_to_menu", "id": str(call.message.id)}))
        keyboard.add(button_1)

        bot.edit_message_text(text='Настройки сохранены.', chat_id=call.message.chat.id, message_id=int(info['id']), reply_markup=keyboard)

    if info['changing'] == 'go_to_menu':
        keyboard = telebot.types.InlineKeyboardMarkup()

        button_1 = telebot.types.InlineKeyboardButton('Расположение', callback_data=json.dumps(
            {"changing": "place", "id": str(call.message.id)}))
        button_2 = telebot.types.InlineKeyboardButton('Шрифт', callback_data=json.dumps(
            {"changing": "font", "id": str(call.message.id)}))
        keyboard.add(button_1, button_2)

        bot.edit_message_text(text='Настройки:', chat_id=call.message.chat.id, message_id=int(info['id']),
                              reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])
def main(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    src = time.strftime(r'[%Y_%m_%d] %H`%M`%S')+randomHex()+'.png'

    with open(f'{directory}\\Images\\{src}', 'wb') as new_file:
        new_file.write(downloaded_file)

    #bot.send_message(message.chat.id, 'Создаём ржомбу...')
    if not os.path.exists(f'Results\\{message.chat.username}'):
        os.makedirs(f'Results\\{message.chat.username}')
        
    MemeGenerator.generate(f'Images\\{src}', f'Results\\{message.chat.username}\\{src}', message.caption,
                           Settings.place.get(message.chat.id), Settings.font.get(message.chat.id))
    sendImage(message.chat.id, f'Results\\{message.chat.username}\\{src}', message.message_id)
    counter.inc()

bot.polling(none_stop=True, interval=0)
