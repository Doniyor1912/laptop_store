from telebot import TeleBot
from telebot.types import LabeledPrice

from config.config import Config
from data_base.laptop_db import Postgresql_laptop
from data_base.smartwatch_db import Postgresql_smartwatch
from data_base.tv_db import Postgresql_tv
from keyboard import *
from language.lang_bot import *


click_token = Config().click_token
token = Config().token
bot = TeleBot(token)

user_langs = {}


@bot.message_handler(commands=['start'])
def start(messsage):
    chat_id = messsage.chat.id
    first_name = messsage.from_user.first_name
    bot.send_message(chat_id,f" Salom {first_name}\nBotga xush kelibsiz!")
    localizatsiya(messsage)

def localizatsiya(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Tilni tanlang!",reply_markup=generation_keyboard())

    bot.register_next_step_handler(message,main_menu)



def main_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id)

    if message.text == '🇺🇿UZ':
        lang = "uz"
        bot.send_message(chat_id, choose_catalog[lang], reply_markup=generate_catalog(lang))

    if message.text == '🇷🇺RU':
        lang = "ru"
        bot.send_message(chat_id, choose_catalog[lang], reply_markup=generate_catalog(lang))

    if message.text == '🇬🇧EN':
        lang = "en"
        bot.send_message(chat_id, choose_catalog[lang], reply_markup=generate_catalog(lang))

    if message.text == '/start':
        return start(message)

    user_langs[chat_id] = lang
    bot.register_next_step_handler(message,main_catalogs)

def main_catalogs(message, product_id=0, products=None):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id)
    if message.text == main_block[lang]:
        return start(message)

    if message.text == change_lang[lang]:
        return localizatsiya(message)

    if message.text == laptop[lang]:
        products = Postgresql_laptop().select_data()

    if message.text == smartwatch[lang]:
        products = Postgresql_smartwatch().select_data()

    if message.text == television[lang]:
        products = Postgresql_tv().select_data()

    if message.text == forword[lang] and product_id < len(products):
        product_id += 1

    elif message.text == back[lang] and product_id > 0:
        product_id -= 1

    product = products[product_id]

    product_title = product[0]
    product_url = product[1]
    image = product[2]
    price = product[3]


    bot.send_photo(chat_id, image, caption=f'\n{product_name[lang]}: {product_title}'
                                           f'\n\n{product_price1[lang]}: {price}',
                                           reply_markup=generate_inline_url(product_url,lang))

    user_message = bot.send_message(chat_id, f"{count_product[lang]} : {len(products) - (product_id + 1)}", reply_markup=generate_pagination(lang))

    if message.text ==forword[lang] and len(products) - (product_id + 1) == 0:
        bot.delete_message(chat_id, message.id + 2)
        bot.send_message(chat_id, reply_product[lang], reply_markup=generate_pagination(lang))
        product_id = product_id - len(products) # -1
        # print(product_id)

    bot.register_next_step_handler(user_message, main_catalogs, product_id, products)

@bot.callback_query_handler(func=lambda call: True)
def get_callback_data(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id)
    if call.data == "buy":
        product_info = call.message.caption.split(": ")
        product_price = ""
        price = product_info[-1].replace('UZS', "")
        for x in price:
            if x.isdigit():
                product_price += x

        INVOICE = {
            "title": product_info[1],
            "description": product_info[1],
            "invoice_payload": "bot-defined invoice payload",
            "provider_token": click_token,
            "start_parameter": "pay",
            "currency": "UZS",
            "prices": [LabeledPrice(label=product_info[1], amount=int(product_price + "00"))],
        }

        bot.send_invoice(chat_id, **INVOICE)

@bot.pre_checkout_query_handler(func=lambda query: True)
def invoice_checkout(query):
    query_id = query.id
    lang = user_langs.get(query_id)
    """ Проверка чека """
    bot.answer_pre_checkout_query(query_id, ok=True, error_message=error_message[lang])


bot.polling()




