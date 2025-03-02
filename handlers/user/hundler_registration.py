from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards.user import keyboard_registration as kb
from utils.error_handling import error_handler
from utils.send_admins import send_message_admins_text, send_message_admins_media_group

from datetime import datetime
from database import requests as rq
from database.models import User
from config_data.config import Config, load_config
import logging

router = Router()
config: Config = load_config()


class StateRegistration(StatesGroup):
    fullname = State()
    age = State()


@router.callback_query(F.data == 'start_yes')
@error_handler
async def process_start_yes(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Начало регистрации
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_start_yes')
    if await rq.get_user_registration(tg_id=callback.from_user.id):
        await callback.message.edit_text(text="Любое, даже маленькое и полезное дело может быть утомительно на"
                                              " ежедневной основе. Поэтому PP Lab Bot призван мотивировать вас и"
                                              " помогать не бросать прием коллагена на полпути. Ведь только регулярный"
                                              " прием препарата даст видимый результат и укрепит ваше здоровье.\n"
                                              "⬇️⬇️⬇️\n"
                                              "🔹За каждый своевременный прием коллагена вы будете получать 50"
                                              " бонусных баллов.\n"
                                              "🔹В случае пропуска приема вы будете терять 10 бонусных баллов.\n"
                                              "Соблюдайте дисциплину и копите бонусные баллы. В личном кабинете"
                                              " на сайте https://pplab.ru/ вы можете следить за количеством баллов"
                                              " и обменивать их на продукцию PP Lab.\n"
                                              "🎁Это поможет вам сэкономить при покупке новой упаковки коллагена."
                                              " Не упустите эту прекрасную возможность!""",
                                         reply_markup=kb.keyboard_start_registration())
    else:
        await callback.message.edit_text(text="""Укажите, где вы приобрели коллаген PP Lab.""",
                                         reply_markup=kb.keyboard_select_marketplace())
    await callback.answer()


@router.callback_query(F.data == 'done_continue')
@error_handler
async def done_continue(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем нажатие клавиши
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('done_continue')
    await callback.message.edit_text(text="""Отлично! Давайте познакомимся. Как вас зовут?""")
    await state.set_state(StateRegistration.fullname)
    await callback.answer()


@router.message(F.text, StateFilter(StateRegistration.fullname))
@error_handler
async def get_full_name(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем имя пользователя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_name')
    full_name = message.text
    await rq.set_user_full_name(tg_id=message.from_user.id,
                                full_name=full_name)
    await message.answer(text="""Напишите ваш возраст для получения более точных рекомендаций по приему коллагена.""")
    await state.set_state(StateRegistration.age)


@router.message(F.text, StateFilter(StateRegistration.age))
@error_handler
async def get_age(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем имя пользователя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_age')
    age = message.text
    if age.isdigit() and int(age) > 0:
        await rq.set_user_age(tg_id=message.from_user.id,
                              age=int(age))
        await message.answer(text="""Укажите, где вы приобрели коллаген PP Lab.""",
                             reply_markup=kb.keyboard_select_marketplace())
    else:
        await message.answer(text='Данные введены не корректно, повторите ввод')
