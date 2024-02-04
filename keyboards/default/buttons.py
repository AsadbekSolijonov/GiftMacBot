from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Buttons:
    @staticmethod
    def share_contact():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        contact = KeyboardButton('Raqamni yuborish', request_contact=True)
        keyboard.add(contact)
        return keyboard

    @staticmethod
    def start_game_ready():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        start_game = KeyboardButton('O`yinni boshlash')
        keyboard.add(start_game)
        return keyboard

    @staticmethod
    def start_game():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_game = KeyboardButton('Boshlash')
        keyboard.add(start_game)
        return keyboard

    @staticmethod
    def next_select():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        next_ = KeyboardButton('Keyingisi')
        select = KeyboardButton('Tanlash')
        keyboard.add(next_, select)
        return keyboard

    @staticmethod
    def show_gift():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        gift = KeyboardButton('Sovg`ani ko`rish')
        keyboard.add(gift)
        return keyboard
