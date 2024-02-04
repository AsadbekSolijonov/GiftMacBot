import logging
import random
import time

from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.buttons import Buttons
from loader import dp
from aiogram import types

from states.register import Register, Game
from utils.db_api.database import Clients, Gifts
import datetime
import pytz

timezone = pytz.timezone('Asia/Tashkent')


@dp.message_handler(text=['O`yinni boshlash', 'Keyingisi'])
async def start_game(message: types.Message):
    chat_id = message.chat.id
    client = Clients()
    if not client.has_client_id(chat_id):
        await message.answer("O`yin boshlashni birinchi qoidasi <b>Ismingizni</b> kiriting:",
                             reply_markup=ReplyKeyboardRemove())
        await Register.name.set()
    else:
        max_attempt = 2
        all_gifts = Gifts().all_gifts()
        if all_gifts:
            chat_id = message.chat.id
            clients = Clients()
            try:
                attempt, status = clients.how_attempt_status(chat_id=chat_id)
                if attempt < 3 and status == 'open':
                    choose = all_gifts[random.randint(0, len(all_gifts) - 1)][1]
                    msg = await message.answer(f'{choose.upper()}')
                    await shuffle_algo(message, msg, choose, all_gifts)
                    await message.answer('🎁')
                    if max_attempt - attempt == 0:
                        await message.answer(
                            '<b>Barcha imkoniyatdan foydalanib bo`ldingiz.</b>\nSovg`ani ko`rish uchun tugmani bosing.',
                            reply_markup=Buttons.show_gift())
                    else:
                        await message.answer(
                            f'Sizda <b>{max_attempt - attempt}</b> urinish bor xohlasangiz shu yerda butunlay to`xtishingiz mumkin.',
                            reply_markup=Buttons().next_select())
                else:
                    await message.answer(
                        '<b>Barcha imkoniyatdan foydalanib bo`ldingiz.</b>\nSovg`ani ko`rish uchun tugmani bosing.',
                        reply_markup=Buttons.show_gift())
            except Exception as e:
                logging.warning(f'{e}')
                await message.answer("<b>Botni qaytadan ishga tushuring: /start</b>")
        else:
            await message.answer('<b>Hali sovg`alar qo`shilmagan bu haqida adminga habar bering.</b>\n\n'
                                 f'<b>Bog`lanish uchun:</b>'
                                 f'\n\t<b>Chat: <a href="https://t.me/macshop_admin">Admin </a></b>'
                                 f'\n\t<b>Kanal: <a href="https://t.me/macshop_uz">Macshop.uz</a></b>')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Register.name)
async def get_name(message: types, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(
        '<b>Raqamingizni ulashing</b>\nbu siz bilan bog`lanishimiz uchun kerak!',
        reply_markup=Buttons.share_contact())
    await Register.contact.set()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Register.contact)
async def get_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        name = data.get('name')
        contact = message.contact.phone_number
        clients = Clients()
        clients.insert_clients(chat_id=message.chat.id, name=name, contact=contact)
    await message.answer("Ma`lumotlar qabul qilindi.\nO`yinni boshlash uchun tugmani bosing!",
                         reply_markup=Buttons.start_game_ready())
    await state.finish()


async def shuffle_algo(message, msg, choose, all_gifts):
    clients = Clients()
    choose = None
    chat_id = message.chat.id
    count = None
    if len(Gifts().all_gifts()) == 1:
        count = 1
    else:
        count = 3
    for gift in range(count):
        try:
            choose = all_gifts[random.randint(0, len(all_gifts) - 1)]
            await msg.edit_text(f"<b>{choose[1].upper()}</b>")
        except Exception as e:
            return await shuffle_algo(message, msg, choose, all_gifts)
        time.sleep(0.3)
    clients.update_clients(chat_id=chat_id, gift=choose[1], day=datetime.datetime.now(timezone))
    attempt, status = clients.how_attempt_status(chat_id=chat_id)
    if attempt < 3 and status == 'open':
        if attempt == 2:
            clients.update_clients(chat_id=chat_id, status='close')
        clients.plus_attempt(chat_id=chat_id)


@dp.message_handler(text=['Sovg`ani Tanlash'])
async def selected_gift(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    clients = Clients()
    clients.update_clients(chat_id=chat_id, status='close')
    await message.answer('Sizning urinishlaringiz butunlay tugadi.',
                         reply_markup=Buttons.show_gift())


@dp.message_handler(text=['Sovg`ani ko`rish'])
async def show_my_gift(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    clients = Clients()
    has_gift, has_status, day = clients.find_gift(chat_id=chat_id)
    if has_gift and has_status == 'close':
        await message.answer(
            f'Sizning sovg`angiz <tg-spoiler>🎁<b>{has_gift.upper()}</b>🎁</tg-spoiler>\n'
            f'<b>Kuni: {day[:16]}</b> \nSovg`ani faqat bugun harid qilgan '
            f'vaqtingizda qo`lga kiritishingiz mumkin ertasiga sovg`angiz kuyib ketadi.\n\n'
            f'<b>Bog`lanish uchun:</b>'
            f'\n\t<b>Chat: <a href="https://t.me/macshop_admin">Admin </a></b>'
            f'\n\t<b>Kanal: <a href="https://t.me/macshop_uz">Macshop.uz</a></b>')
    elif has_gift and has_status == 'open':
        await message.answer(
            f'Sizning sovg`angiz <tg-spoiler>🎁<b>{has_gift.upper()}</b>🎁</tg-spoiler>'
            f'\nLekin davom ettirish imkoningiz bor.',
            reply_markup=Buttons.next_select())
