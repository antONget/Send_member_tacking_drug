import datetime

from aiogram.types import CallbackQuery, Message
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user import keyboard_main_menu as kb
from utils.error_handling import error_handler
from filter.filter import validate_time
from config_data.config import Config, load_config
from database.models import Drug
from database import requests as rq
import logging

router = Router()
config: Config = load_config()


class StateMainMenu(StatesGroup):
    change_time = State()


@router.message(F.text == 'Главное меню')
@error_handler
async def get_marketplace(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка нажатия главного меню
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_name')
    await message.answer(text='Выберите раздел',
                         reply_markup=kb.keyboard_start_menu())


@router.callback_query(F.data.startswith('main_menu_'))
@error_handler
async def get_action_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем вид препарата
    :param callback: main_menu_balance | main_menu_time
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_action_main_menu')
    action = callback.data.split('_')[-1]
    if action == 'balance':
        info_user = await rq.get_user_by_id(tg_id=callback.from_user.id)
        await callback.message.edit_text(text=f'Ваш баланс составляет: {info_user.balance_user} баллов')
    elif action == 'time':
        drug_active: Drug = await rq.get_drug_active_tg_id(tg_id=callback.from_user.id)
        if drug_active:
            time = drug_active.time_tacking
            taste_drug = drug_active.taste_drug
            volume_drug = drug_active.volume_drug
            taste = 'грейпфрута'
            if taste_drug == 'limon':
                taste = 'лимона'
            elif taste_drug == 'orange':
                taste = 'апельсина'
            await state.update_data(drug_id_change=drug_active.id)
            await callback.message.edit_text(text=f'Ваше время приема коллагена: Collagen Jelly PP Lab со вкусом'
                                                  f' {taste} - {volume_drug} саше <b>{time}</b>',
                                             reply_markup=kb.keyboard_change_time())
        else:
            await callback.message.edit_text(text=f'У вас нет активных курсов приема коллагена')
    await callback.answer()


@router.callback_query(F.data == 'change_time')
@error_handler
async def date_start_taking_drug(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обновление времени приема коллагена
    :param callback: date_start_change
    :param state:
    :param bot:
    :return:
    """
    logging.info('date_start_taking_drug')
    await callback.message.edit_text(text="📃Употреблять коллаген следует за 30 минут до еды один раз в день "
                                          "(утром, днем или вечером). В какое время вам будет удобно принимать"
                                          " коллаген? Введите свой ответ ниже в формате “10:00”")
    await state.set_state(StateMainMenu.change_time)


@router.message(F.text, StateFilter(StateMainMenu.change_time))
@error_handler
async def get_age(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем удобное время для приема коллагена
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_age')
    time_start_taking_drug = message.text
    if validate_time(time_start_taking_drug):
        await message.answer(text='Время приема коллагена обновлено')
        data = await state.get_data()
        drug_id_change = data['drug_id_change']
        await rq.set_drug_time_tacking(drug_id=drug_id_change,
                                       time_tacking=time_start_taking_drug)
    else:
        await message.answer(text="""Некорректно указано время. Введите свой ответ ниже в формате “10:00”""")

