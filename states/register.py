from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    contact = State()


class Game(StatesGroup):
    game = State()
