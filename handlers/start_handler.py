from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter, or_f, CommandObject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import start_keyboard as kb
from config_data.config import Config, load_config
from database import requests as rq
from database.models import User
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin

import logging
from datetime import datetime

router = Router()
config: Config = load_config()


class PersonalData(StatesGroup):
    fullname = State()
    personal_account = State()
    phone = State()


@router.message(CommandStart())
@error_handler
async def process_start_command_user(message: Message, state: FSMContext, command: CommandObject, bot: Bot) -> None:
    """
    Обработки запуска бота или ввода команды /start
    :param message:
    :param state:
    :param command:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.set_state(state=None)
    qr = command.args
    # добавление пользователя в БД если еще его там нет
    user: User = await rq.get_user_by_id(tg_id=message.from_user.id)
    if not user:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "user_name"
        data_user = {"tg_id": message.from_user.id,
                     "username": username,
                     "qr": qr}
        await rq.add_user(data=data_user)
    else:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "user_name"
        data_user = {"tg_id": message.from_user.id,
                     "username": username,
                     "qr": qr}
        await rq.add_user(data=data_user)
    if await check_super_admin(telegram_id=message.from_user.id):
        await message.answer(text='PP Lab Bot — ваш помощник для достижения красоты и здоровья изнутри. '
                                  'Я буду напоминать вам о своевременном приеме коллагена'
                                  ' и поддерживать вас на этом пути🙏.\n'
                                  '<b>Вы администратор проекта</b>',
                             reply_markup=kb.keyboard_start_admin())
    else:
        await message.answer(text='PP Lab Bot — ваш помощник для достижения красоты и здоровья изнутри. '
                                  'Я буду напоминать вам о своевременном приеме коллагена'
                                  ' и поддерживать вас на этом пути🙏.',
                             reply_markup=kb.keyboard_start_())
    await message.answer(text='Нажмите “Да”, если вы готовы начать прием препарата.',
                         reply_markup=kb.keyboard_start())
