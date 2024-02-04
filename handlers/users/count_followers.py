from loader import dp
from aiogram import types

from utils.db_api.database import Clients


@dp.message_handler(commands='followers')
async def all_followers(message: types.Message):
    followers = Clients().all_clients()[0]
    if followers:
        await message.answer(f'🔔 Ro`yxatdan o`tgan <b>Obunachilar</b> soni: <tg-spoiler><b>{followers}</b></tg-spoiler> ta.')
    else:
        await message.answer(f'Ro`yxatdan o`tgan obunachilar hali mavjud emas!')