from telebot import types
from  language.lang_bot import *

def generation_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_ru = types.KeyboardButton(text="🇷🇺RU")
    btn_uz = types.KeyboardButton(text="🇺🇿UZ")
    btn_eng = types.KeyboardButton(text="🇬🇧EN")
    return keyboard.row(btn_ru,btn_uz,btn_eng)


def generate_catalog(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_laptops = types.KeyboardButton(text=laptop[lang])
    btn_smartwatch = types.KeyboardButton(text=smartwatch[lang])
    btn_TV = types.KeyboardButton(text=television[lang])
    btn_lan = types.KeyboardButton(text=change_lang[lang])
    keyboard.row(btn_smartwatch, btn_laptops, btn_TV)
    keyboard.row(btn_lan)
    return keyboard


def generate_inline_url(url,lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton(text=purchase[lang], callback_data="buy")
    btn_url = types.InlineKeyboardButton(text=all_inform[lang], url=url)
    keyboard.row(btn_buy, btn_url)
    return keyboard


def generate_pagination(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    step_go = types.KeyboardButton(text=forword[lang])
    step_back = types.KeyboardButton(text=back[lang])
    step_back_menu = types.KeyboardButton(text=main_block[lang])
    keyboard.row(step_go,step_back)
    keyboard.row(step_back_menu)
    return keyboard