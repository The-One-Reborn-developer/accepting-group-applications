import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.orm import Application
from bot.telegram_api.requests import send_notification


class ApplicationFSM(StatesGroup):
    username = State()
    link = State()
    description = State()
    category = State()


start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ApplicationFSM.username)
    await state.update_data(
        username=f'https://t.me/{message.from_user.username}')
    await state.set_state(ApplicationFSM.link)

    await message.answer('Пришлите ссылку на группу/канал, которую хотите добавить в список.')


@start_router.message(ApplicationFSM.link)
async def link_handler(message: Message, state: FSMContext):
    link = message.text

    if not link.startswith('https://t.me/'):
        await message.answer('Некорректная ссылка.')
        return

    await state.update_data(link=message.text)
    await state.set_state(ApplicationFSM.description)
    await message.answer('Напишите вкратце описание группы/канала.')


@start_router.message(ApplicationFSM.description)
async def description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(ApplicationFSM.category)
    await message.answer('В какую из существующих категорий в списке Вы хотели бы, чтобы мы добавили группу/канал?'
                         '\n\nЕсли такой категории не существует, можете написать её здесь и обосновать создание новой категории.')


@start_router.message(ApplicationFSM.category)
async def category_handler(message: Message, state: FSMContext):
    await state.update_data(category=message.text)

    application_data = await state.get_data()

    applications_list = Application.get_applications()
    if applications_list == []:
        pass
    elif not applications_list:
        await message.answer('Произошла ошибка при сохранении заявки.'
                             '\n\nПопробуйте ещё раз, подав команду /start или нажмите кнопку в меню.')
        return

    readable_applications_list = [application.to_dict()
                                  for application in applications_list]

    if readable_applications_list:
        for application in readable_applications_list:
            if application['link'] == application_data['link']:
                await state.clear()
                await message.answer(f'Данная группа/канал уже есть в супергруппе.\n\n'
                                     'Если хотите добавить ещё группу/канал, то напишите команду /start или нажмите кнопку в меню.')
                return

    database_result = Application.insert_application(**application_data)

    send_notification_result = await send_notification(application_data)

    if not database_result:
        await state.clear()
        await message.answer('Произошла ошибка при сохранении заявки.'
                             '\n\nПопробуйте ещё раз, подав команду /start или нажмите кнопку в меню.')
        return

    if not send_notification_result:
        await state.clear()
        await message.answer('Произошла ошибка при отправке уведомления.'
                             '\n\nПопробуйте ещё раз, подав команду /start или нажмите кнопку в меню.')
        return

    await state.clear()
    await message.answer('Ваша заявка принята, ожидайте уведомления от бота о добавлении группы/канала или отклонении заявки.'
                         '\n\nТакже Вам могут написать администраторы для уточнения информации.'
                         '\n\nЕсли хотите добавить ещё группу/канал, то напишите команду /start или нажмите кнопку в меню.')


@start_router.callback_query(F.data == 'approve')
async def approve_application(callback: CallbackQuery):
    await callback.message.edit_text(text='Заявка одобрена. Группа/канал добавлен/а в соответствующий раздел.')


@start_router.callback_query(F.data == 'decline')
async def decline_application(callback: CallbackQuery):
    await callback.message.edit_text(text='Заявка отклонена.')
