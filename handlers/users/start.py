from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.buttons import Buttons
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = (f"Assalomu aleykum <b>{message.from_user.full_name}!</b>\n\n"
            f"<b>O'yin Qoidasi:</b>\n\n"
            f"<b>O'yin davomida Sizda 3 ta urinish bor</b>.\n\n<b>1-Qoida:</b> Siz <b>sovg'a tanlash</b> "
            f"yoki <b>davom etish</b> tugmasini tanlashingiz mumkin va ohirgi urinishda "
            f"chiqan sovg'a sizga taqdim e'tilgan sov'ga hissoblanadi. "
            f"\n\n<b>2-Qoida:</b> Agar xohlasangiz o'yinni <b> birinchi</b> yoki <b>ikkinchi</b> urinishda ham "
            f"to'xtatishingiz va chiqqan sovg'angizni tanlashingiz mumkin. "
            f"\n\n<b>3-Qoida:</b> Qo'lga kiritilgan sovg'a faqat shu kunni o'zida "
            f"<b>MACBOOK</b> xaridi uchun qo'shib beriladi.")

    url = 'media/image/logo/logo.jpg'
    with open(url, 'rb') as img:
        await message.answer_photo(img, caption=f"{text}", reply_markup=Buttons.start_game_ready())

    # await message.answer(text, reply_markup=Buttons.start_game_ready())
