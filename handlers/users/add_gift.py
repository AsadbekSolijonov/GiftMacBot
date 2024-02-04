from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp
from aiogram import types

from utils.db_api.database import Gifts


@dp.message_handler(lambda message: message.text.startswith("#add"))
async def add_gift(message: types.Message):
    chat_id = message.chat.id
    if str(chat_id) in ADMINS:
        gift = Gifts()
        msg = message.text.replace('#add', '').strip()
        if gift.has_gift(msg):
            await message.answer('Bu mahsulotni qo`sha olmaysiz!\nChunki bu mahsulot avval qo`shilgan!')
        else:
            Gifts().insert_gift(msg)
            await message.answer('Mahsulot Gifts bo`limiga qo`shildi.\nKo`rish uchun: /gifts')
    else:
        await message.answer('Kechirasiz sizga ruxsat yo`q!')


@dp.message_handler(lambda message: message.text.startswith("#del"))
async def delete_gift(message: types.Message):
    chat_id = message.chat.id
    if str(chat_id) in ADMINS:
        gift = Gifts()
        msg = message.text.replace('#del', '').strip()
        if gift.has_gift_by_id(msg):
            Gifts().delete_gift(msg)
            await message.answer(f'{msg} raqamli sovg`a o`chirildi!\nKo`rish uchun: /gifts')
        else:
            await message.answer(f'{msg} raqamli sovg`a topilmadi.\nKo`rish uchun: /gifts')
    else:
        await message.answer('Kechirasiz sizga ruxsat yo`q!')


@dp.message_handler(commands=['gifts'])
async def all_gifts(message: types.Message):
    chat_id = message.chat.id
    gifts = Gifts()
    datas = gifts.all_gifts()
    if str(chat_id) in ADMINS:
        if datas:
            text = ("<b>Sovg`alar:</b>\n\n"
                    "<b>Agar sovg`a <code>qo`shimoqchi</code> bo`lsangiz:</b>.\n"
                    "<tg-spoiler><b>#add sovg`a_nomi</b></tg-spoiler> - <i>deb sovg`a nomini yozsangiz qo`shiladi.</i>\n\n"
                    "<b>Agar sovg`ani  <code>o`chirmoqchi</code> bo`lsangiz:</b>\n"
                    "<tg-spoiler><b>#del 10</b></tg-spoiler> - <i>deb sovg`a nomerini yozsangiz o`chib ketadi.</i>\n\n")
            for gift_id, gift_name in datas:
                text += f'<b>{gift_id}</b>. {gift_name}\n'
            await message.answer(text, reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(
                "<b>Hozircha hech qanday sovg`a qo`shilmagan.</b>\n\n"
                "Agar sovg`a qo`shimoqchi bo`lsangiz:\n"
                "<tg-spoiler><b>#add sovg`a_nomi</b></tg-spoiler> - deb sovg`a nomini yozsangiz qo`shiladi.\n\n"
                "Agar sovg`ani  o`chirmoqchi bo`lsangiz:\n"
                "<tg-spoiler><b>#del 10</b></tg-spoiler> - deb sovg`a nomerini yozsangiz o`chib ketadi.",
                reply_markup=ReplyKeyboardRemove())
    else:
        if datas:
            await message.answer(f'🎁 Sovg`lar soni: {len(datas)} ta.', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(
                '<b>Hali sovg`alar qo`shilmagan bu haqida adminga habar bering.</b>\n\n'
                f'<b>Bog`lanish uchun:</b>'
                f'\n\t<b>Chat: <a href="https://t.me/macshop_admin">Admin </a></b>'
                f'\n\t<b>Kanal: <a href="https://t.me/macshop_uz">Macshop.uz</a></b>',
                reply_markup=ReplyKeyboardRemove())
