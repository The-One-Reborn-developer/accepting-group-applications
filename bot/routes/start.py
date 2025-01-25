from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.orm import DatabaseManager, Application


class ApplicationFSM(StatesGroup):
    username = State()
    link = State()
    description = State()
    category = State()


DATABASE = DatabaseManager()
DATABASE.create_tables()
start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ApplicationFSM.username)
    await state.update_data(
        username=f'https://t.me/{message.from_user.username}')
    await state.set_state(ApplicationFSM.link)

    await message.answer('Пришлите ссылку на группу, которую хотите добавить в список.')


@start_router.message(ApplicationFSM.link)
async def link_handler(message: Message, state: FSMContext):
    link = message.text

    if not link.startswith('https://t.me/'):
        await message.answer('Некорректная ссылка.')
        return

    await state.update_data(link=message.text)
    await state.set_state(ApplicationFSM.description)
    await message.answer('Напишите вкратце описание группы.')


@start_router.message(ApplicationFSM.description)
async def description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(ApplicationFSM.category)
    await message.answer('В какую из существующих категорий в списке Вы хотели бы, чтобы мы добавили группу?'
                         '\n\nЕсли такой категории не существует, можете написать её здесь и обосновать.')


@start_router.message(ApplicationFSM.category)
async def category_handler(message: Message, state: FSMContext):
    await state.update_data(category=message.text)

    application_data = await state.get_data()
    database_result = Application.insert_application(
        ** application_data)

    if not database_result:
        await message.answer('Произошла ошибка при сохранении заявки.'
                             '\n\nПопробуйте ещё раз, подав команду /start или нажмите кнопку в меню.')
        return

    await state.clear()
    await message.answer('Ваша заявка принята, ожидайте уведомления от бота о добавлении группы или отклонении заявки.'
                         '\n\nТакже Вам могут написать администраторы для уточнения информации.'
                         '\n\nЕсли хотите добавить ещё группу, то напишите команду /start или нажмите кнопку в меню.')
