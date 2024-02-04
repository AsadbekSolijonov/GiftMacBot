from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.buttons import Buttons
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = (f"Assalomu aleykum <b>{message.from_user.full_name}!</b>\n\n"
            f"<b>O'yin Qoidasi:</b>\n\n"
            f"<b>O'yin davomida Sizda 3 ta urinish bor</b>. Siz <b>sovg'a</b> "
            f"yoki <b>davom etish</b> tugmasini tanlashingiz mumkin va ohirgi urinishda "
            f"chiqan sovg'a sizga taqdim e'tilgan sov'ga hissoblanadi. "
            f"Agar xohlasangiz o'yinni <b> birinchi</b> yoki <b>ikkinchi</b> urinishda ham "
            f"to'xtatishingiz va chiqqan sovg'angizni tanlashingiz mumkin.")
    await message.answer(text, reply_markup=Buttons.start_game_ready())
