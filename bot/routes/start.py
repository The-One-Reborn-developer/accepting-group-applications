from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Application(StatesGroup):
    user_data = State()
    link = State()
    description = State()
    category = State()


start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Application.user_data)

    await message.answer(f'https://t.me/{message.from_user.username}')
